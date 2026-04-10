[View this page](https://behave.readthedocs.io/en/stable/_sources/index.rst.txt "View this page")

Toggle table of contents sidebar

## Welcome to behave![¶](#welcome-to-behave "Link to this heading")

behave is behaviour-driven development, Python style.

![behave\_logo](https://behave.readthedocs.io/en/stable/_images/behave_logo1.png)

Behavior-driven development (or BDD) is an agile software development technique that encourages collaboration between developers, QA and non-technical or business participants in a software project. We have a page further describing this [philosophy](https://behave.readthedocs.io/en/stable/philosophy/).

[behave](https://pypi.org/project/behave) uses tests written in a natural language style, backed up by Python code.

Once you’ve [installed](https://behave.readthedocs.io/en/stable/install/) _behave_, we recommend reading the

*   [tutorial](https://behave.readthedocs.io/en/stable/tutorial/) first and then
    
*   [feature test setup](https://behave.readthedocs.io/en/stable/gherkin/),
    
*   [behave API](https://behave.readthedocs.io/en/stable/api/) and
    
*   [related software](https://behave.readthedocs.io/en/stable/appendix.related/) (things that you can combine with [behave](https://pypi.org/project/behave))
    
*   finally: [how to use and configure](https://behave.readthedocs.io/en/stable/behave/) the [behave](https://pypi.org/project/behave) tool.
    

There is also a [comparison](https://behave.readthedocs.io/en/stable/comparison/) with the other tools available.

## Contents[¶](#contents "Link to this heading")

*   [Installation](https://behave.readthedocs.io/en/stable/install/)
    *   [Using pip (or …)](https://behave.readthedocs.io/en/stable/install/#using-pip-or)
    *   [Using a Source Distribution](https://behave.readthedocs.io/en/stable/install/#using-a-source-distribution)
    *   [Using the GitHub Repository](https://behave.readthedocs.io/en/stable/install/#using-the-github-repository)
    *   [Optional Dependencies](https://behave.readthedocs.io/en/stable/install/#optional-dependencies)
    *   [Specify Dependency to “behave”](https://behave.readthedocs.io/en/stable/install/#specify-dependency-to-behave)
*   [Tutorial](https://behave.readthedocs.io/en/stable/tutorial/)
    *   [Features](https://behave.readthedocs.io/en/stable/tutorial/#features)
    *   [Feature Files](https://behave.readthedocs.io/en/stable/tutorial/#feature-files)
    *   [Python Step Implementations](https://behave.readthedocs.io/en/stable/tutorial/#python-step-implementations)
    *   [Environmental Controls](https://behave.readthedocs.io/en/stable/tutorial/#environmental-controls)
    *   [Controlling Things With Tags](https://behave.readthedocs.io/en/stable/tutorial/#controlling-things-with-tags)
    *   [Works In Progress](https://behave.readthedocs.io/en/stable/tutorial/#works-in-progress)
    *   [Fixtures](https://behave.readthedocs.io/en/stable/tutorial/#fixtures)
    *   [Debug-on-Error (in Case of Step Failures)](https://behave.readthedocs.io/en/stable/tutorial/#debug-on-error-in-case-of-step-failures)
*   [Behavior Driven Development](https://behave.readthedocs.io/en/stable/philosophy/)
    *   [BDD practices](https://behave.readthedocs.io/en/stable/philosophy/#bdd-practices)
    *   [Outside–in](https://behave.readthedocs.io/en/stable/philosophy/#outsidein)
    *   [The Gherkin language](https://behave.readthedocs.io/en/stable/philosophy/#the-gherkin-language)
    *   [Programmer-domain examples and behavior](https://behave.readthedocs.io/en/stable/philosophy/#programmer-domain-examples-and-behavior)
    *   [Using mocks](https://behave.readthedocs.io/en/stable/philosophy/#using-mocks)
    *   [Acknowledgement](https://behave.readthedocs.io/en/stable/philosophy/#acknowledgement)
*   [Feature Testing Setup](https://behave.readthedocs.io/en/stable/gherkin/)
    *   [Feature Testing Layout](https://behave.readthedocs.io/en/stable/gherkin/#feature-testing-layout)
    *   [Gherkin: Feature Testing Language](https://behave.readthedocs.io/en/stable/gherkin/#gherkin-feature-testing-language)
*   [Tag Expressions](https://behave.readthedocs.io/en/stable/tag_expressions/)
    *   [Tag-Expressions v2](https://behave.readthedocs.io/en/stable/tag_expressions/#tag-expressions-v2)
    *   [Tag Matching with Tag-Expressions](https://behave.readthedocs.io/en/stable/tag_expressions/#tag-matching-with-tag-expressions)
    *   [Select the Tag-Expression Version to Use](https://behave.readthedocs.io/en/stable/tag_expressions/#select-the-tag-expression-version-to-use)
    *   [Tag-Expressions v1](https://behave.readthedocs.io/en/stable/tag_expressions/#tag-expressions-v1)
*   [Using _behave_](https://behave.readthedocs.io/en/stable/behave/)
    *   [Command-Line Arguments](https://behave.readthedocs.io/en/stable/behave/#command-line-arguments)
    *   [Configuration Files](https://behave.readthedocs.io/en/stable/behave/#configuration-files)
*   [Behave API Reference](https://behave.readthedocs.io/en/stable/api/)
    *   [Step Functions](https://behave.readthedocs.io/en/stable/api/#step-functions)
    *   [Environment File Functions](https://behave.readthedocs.io/en/stable/api/#environment-file-functions)
    *   [Fixtures](https://behave.readthedocs.io/en/stable/api/#fixtures)
    *   [Runner Operation](https://behave.readthedocs.io/en/stable/api/#runner-operation)
    *   [Model Objects](https://behave.readthedocs.io/en/stable/api/#model-objects)
    *   [Logging Capture](https://behave.readthedocs.io/en/stable/api/#logging-capture)
    *   [Configuration](https://behave.readthedocs.io/en/stable/api/#configuration)
*   [Fixtures](https://behave.readthedocs.io/en/stable/fixtures/)
    *   [Providing a Fixture](https://behave.readthedocs.io/en/stable/fixtures/#providing-a-fixture)
    *   [Using a Fixture](https://behave.readthedocs.io/en/stable/fixtures/#using-a-fixture)
    *   [Fixture Cleanup Points](https://behave.readthedocs.io/en/stable/fixtures/#fixture-cleanup-points)
    *   [Fixture Setup/Cleanup Semantics](https://behave.readthedocs.io/en/stable/fixtures/#fixture-setup-cleanup-semantics)
    *   [Ensure Fixture Cleanups with Fixture Setup Errors](https://behave.readthedocs.io/en/stable/fixtures/#ensure-fixture-cleanups-with-fixture-setup-errors)
    *   [Composite Fixtures](https://behave.readthedocs.io/en/stable/fixtures/#composite-fixtures)
*   [Userdata](https://behave.readthedocs.io/en/stable/userdata/)
    *   [Overview](https://behave.readthedocs.io/en/stable/userdata/#overview)
    *   [Basic Usage](https://behave.readthedocs.io/en/stable/userdata/#basic-usage)
    *   [Type Converters](https://behave.readthedocs.io/en/stable/userdata/#type-converters)
    *   [Advanced Use Cases](https://behave.readthedocs.io/en/stable/userdata/#advanced-use-cases)
*   [Django Test Integration](https://behave.readthedocs.io/en/stable/usecase_django/)
    *   [Manual Integration](https://behave.readthedocs.io/en/stable/usecase_django/#manual-integration)
    *   [Strategies and Tooling](https://behave.readthedocs.io/en/stable/usecase_django/#strategies-and-tooling)
*   [Flask Test Integration](https://behave.readthedocs.io/en/stable/usecase_flask/)
    *   [Integration Example](https://behave.readthedocs.io/en/stable/usecase_flask/#integration-example)
    *   [Strategies and Tooling](https://behave.readthedocs.io/en/stable/usecase_flask/#strategies-and-tooling)
*   [Practical Tips on Testing](https://behave.readthedocs.io/en/stable/practical_tips/)
    *   [Seriously, Don’t Test the User Interface](https://behave.readthedocs.io/en/stable/practical_tips/#seriously-don-t-test-the-user-interface)
    *   [Automation Libraries](https://behave.readthedocs.io/en/stable/practical_tips/#automation-libraries)
*   [Comparison With Other Tools](https://behave.readthedocs.io/en/stable/comparison/)
    *   [Cucumber](https://behave.readthedocs.io/en/stable/comparison/#cucumber)
    *   [Lettuce](https://behave.readthedocs.io/en/stable/comparison/#lettuce)
    *   [Freshen](https://behave.readthedocs.io/en/stable/comparison/#freshen)
*   [New and Noteworthy](https://behave.readthedocs.io/en/stable/new_and_noteworthy/)
    *   [Noteworthy in Version 1.3.2](https://behave.readthedocs.io/en/stable/new_and_noteworthy_v1.3.2/)
    *   [Noteworthy in Version 1.3.0](https://behave.readthedocs.io/en/stable/new_and_noteworthy_v1.3.0/)
    *   [Noteworthy in Version 1.2.7](https://behave.readthedocs.io/en/stable/new_and_noteworthy_v1.2.7/)
    *   [Noteworthy in Version 1.2.6](https://behave.readthedocs.io/en/stable/new_and_noteworthy_v1.2.6/)
    *   [Noteworthy in Version 1.2.5](https://behave.readthedocs.io/en/stable/new_and_noteworthy_v1.2.5/)
    *   [Noteworthy in Version 1.2.4](https://behave.readthedocs.io/en/stable/new_and_noteworthy_v1.2.4/)
*   [More Information about Behave](https://behave.readthedocs.io/en/stable/more_info/)
    *   [Tutorials](https://behave.readthedocs.io/en/stable/more_info/#tutorials)
    *   [Books](https://behave.readthedocs.io/en/stable/more_info/#books)
    *   [Presentation Videos](https://behave.readthedocs.io/en/stable/more_info/#presentation-videos)
    *   [Tool-oriented Tutorials](https://behave.readthedocs.io/en/stable/more_info/#tool-oriented-tutorials)
    *   [Find more Information](https://behave.readthedocs.io/en/stable/more_info/#find-more-information)
    *   [Get Involved](https://behave.readthedocs.io/en/stable/more_info/#get-involved)
*   [Contributing](https://behave.readthedocs.io/en/stable/contributing/)
    *   [Using `invoke` for Development](https://behave.readthedocs.io/en/stable/contributing/#using-invoke-for-development)
    *   [Update Gherkin Language Specification](https://behave.readthedocs.io/en/stable/contributing/#update-gherkin-language-specification)
    *   [Update Documentation](https://behave.readthedocs.io/en/stable/contributing/#update-documentation)
*   [Appendix](https://behave.readthedocs.io/en/stable/appendix/)
    *   [Formatters and Reporters](https://behave.readthedocs.io/en/stable/appendix.formatters/)
    *   [Runners](https://behave.readthedocs.io/en/stable/appendix.runners/)
    *   [Context Attributes](https://behave.readthedocs.io/en/stable/appendix.context_attributes/)
    *   [Environment Variables](https://behave.readthedocs.io/en/stable/appendix.environment_variables/)
    *   [Status Values](https://behave.readthedocs.io/en/stable/appendix.status/)
    *   [Parse Expressions](https://behave.readthedocs.io/en/stable/appendix.parse_expressions/)
    *   [Cucumber-Expressions](https://behave.readthedocs.io/en/stable/appendix.cucumber_expressions/)
    *   [Regular Expressions](https://behave.readthedocs.io/en/stable/appendix.regular_expressions/)
    *   [Testing Domains](https://behave.readthedocs.io/en/stable/appendix.test_domains/)
    *   [Behave Ecosystem](https://behave.readthedocs.io/en/stable/appendix.behave_ecosystem/)
    *   [Software that Enhances _behave_](https://behave.readthedocs.io/en/stable/appendix.related/)

See also

*   [behave.example](https://github.com/behave/behave.example): [Behave Examples and Tutorials](https://behave.github.io/behave.example/) (HTML)
    
*   Peter Parente: [BDD and Behave](https://tott-meetup.readthedocs.io/en/latest/sessions/behave.html) (tutorial)
    

## Indices and tables[¶](#indices-and-tables "Link to this heading")

*   [Index](https://behave.readthedocs.io/en/stable/genindex/)
    
*   [Module Index](https://behave.readthedocs.io/en/stable/py-modindex/)
    
*   [Search Page](https://behave.readthedocs.io/en/stable/search/)