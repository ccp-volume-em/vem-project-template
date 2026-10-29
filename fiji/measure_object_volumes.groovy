#@ File (label = "Label image (TIFF)", style = "file") labelFile
#@ File (label = "Output folder", style = "directory") outputDir
#@ Boolean (label = "Require physical calibration", value = true, description = "Stop if the image has no voxel size, rather than reporting volumes in voxels") requireCalibration
#@ LogService log
#@output Integer objectCount

/*
 * Measure the physical volume of every labelled object in a 3D label image.
 *
 * Input:  a TIFF label image, where 0 is background and each other value is
 *         one object. Its voxel size (Image > Properties) must be set.
 * Output: object_volumes.csv, with the volume of each object in cubic
 *         calibration units (e.g. nm³), and provenance.json, recording the
 *         parameters, input, ImageJ version and this script's checksum.
 *
 * Run it in Fiji (open it and click Run, which shows a dialog for the
 * parameters above), or headless, e.g. on an HPC cluster: see fiji/README.md.
 */

import groovy.json.JsonOutput
import ij.IJ
import java.security.MessageDigest
import java.time.OffsetDateTime

// A virtual stack reads one slice at a time from disk, so volumes larger
// than memory still work. It needs an uncompressed TIFF; otherwise fall back
// to opening the whole image.
def imp = IJ.openVirtual(labelFile.path) ?: IJ.openImage(labelFile.path)
if (imp == null) {
	throw new IllegalArgumentException("Could not open ${labelFile} as an image")
}
if (!(imp.getBitDepth() in [8, 16])) {
	throw new IllegalArgumentException("Labels must be an 8- or 16-bit integer image, not ${imp.getBitDepth()}-bit")
}

def cal = imp.getCalibration()
def unit = cal.getUnit()
if (!cal.scaled()) {
	if (requireCalibration) {
		throw new IllegalArgumentException("${labelFile.name} has no voxel size. Set it in Image > Properties, or untick 'Require physical calibration'.")
	}
	log.warn("${labelFile.name} has no voxel size: volumes are in voxels")
	unit = "voxel"
}

def counts = new TreeMap<Integer, Long>()
def stack = imp.getStack()
for (int z = 1; z <= stack.getSize(); z++) {
	def pixels = stack.getProcessor(z)
	for (int i = 0; i < pixels.getPixelCount(); i++) {
		int label = pixels.get(i)
		if (label != 0) {
			counts[label] = (counts[label] ?: 0L) + 1
		}
	}
}

// Volume EM voxels are often anisotropic, so all three sizes matter.
def voxelVolume = cal.scaled() ? cal.pixelWidth * cal.pixelHeight * cal.pixelDepth : 1.0d

outputDir.mkdirs()
def csvFile = new File(outputDir, "object_volumes.csv")
csvFile.withWriter("UTF-8") { out ->
	out.println(cal.scaled() ? "label,volume_${unit}3" : "label,volume_voxels")
	// Plain notation: Groovy would write large volumes as e.g. 1.96608E7.
	counts.each { label, n -> out.println("${label},${BigDecimal.valueOf(n * voxelVolume).toPlainString()}") }
}

// Fiji passes in the path of the running script under this name.
def scriptFile = new File(binding.variables["javax.script.filename"] ?: "")
def provenance = [
	script    : "measure_object_volumes.groovy",
	// The checksum identifies exactly which version of this script ran.
	sha256    : scriptFile.isFile() ? MessageDigest.getInstance("SHA-256").digest(scriptFile.bytes).encodeHex().toString() : null,
	created   : OffsetDateTime.now().toString(),
	imagej    : IJ.getFullVersion(),
	parameters: [labelFile: labelFile.path, outputDir: outputDir.path, requireCalibration: requireCalibration],
	voxelSize : [x: cal.pixelWidth, y: cal.pixelHeight, z: cal.pixelDepth, unit: unit],
	outputs   : [csvFile.path],
]
new File(outputDir, "provenance.json").setText(JsonOutput.prettyPrint(JsonOutput.toJson(provenance)) + "\n", "UTF-8")

imp.close()
objectCount = counts.size()
log.info("Measured ${objectCount} objects; results in ${csvFile}")
