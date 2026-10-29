# Using generative AI

From the guide: [Software Development → AI use](https://ccp-volume-em.github.io/guide/software/#ai-use)
and [Making software public → Statements about AI use](https://ccp-volume-em.github.io/guide/software_publishing/#statements-about-ai-use).

AI tools can speed development up a lot. Weigh that against the risks: poor
code quality, growing technical debt, and code that nobody on the project
understands.

Read [Responsible use of AI in research software](https://www.software.ac.uk/guide/responsible-use-ai-research-software)
before using generative AI in a project.

## While developing

- Review and test all AI-generated code so it is correct and maintainable.
- Prefer tests that are independent of the generated code and, ideally,
  written by a person.
- Treat generated code like any other external contribution: understand it,
  review it for security and bias, test it, and check for licence or
  attribution concerns.
- AI output can be plausible but wrong. An AI-use statement doesn't replace
  quality assurance.
- Acknowledge AI use in the documentation and in the relevant commits.

## Data protection

- Don't send personal, confidential, security-sensitive or unpublished
  material to an external AI service unless its data-handling terms and your
  project's approvals allow it.
- Follow the policies of your institution, funder, publisher and software
  community.

## Responsibility and authorship

- The human contributors and maintainers are responsible for everything
  released.
- Don't list AI systems as authors or copyright holders.

## AI-use statements

When AI use was substantive, add a short statement to the repository, release
notes or paper. Don't publish confidential prompts or sensitive data. A
statement can say:

- which tool and model (version or access date, if known);
- which parts of the work it helped with;
- whether its output was modified;
- how a person reviewed, tested and validated the result.

Example from the guide:

> Generative AI was used to suggest docstrings and unit-test cases. All
> suggestions were reviewed and edited by the maintainers, and the resulting
> software passed the project's automated tests. No confidential source code or
> research data was provided to the service.

If no generative AI contributed to a release, no statement is normally needed,
unless a policy requires one.
