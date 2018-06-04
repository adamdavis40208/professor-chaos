# professor-chaos
chaos monkey get up t̡̬͔̗̀r̴̴̞̕y͞͏̝̱̞̯̻̩ͅ ҉̮͓̰̻͕̻̺͎̀ͅt̡̡̮͇̙̩̞̝͘ͅo̲̜̰͓̠͝ ̵̼͔̬͙͚̝͎̹̞b̹͚͡r͔̺̣͢͝e̵͔̤̟̺a̪̲̰͉͚̠̪̕͘ͅk̦̣͖͈̺̟̜͓ ͘͏͎̥̟͇̪͍p̵͙͇̖͍͙r̭̱̪͚̘̣̝ͅo̴̱͓̦͜d̵̥͎̞̥̤̰͚u̧͕̹̙̗̝̟̰̘͢͝c̤̦̙̙͎̟͢t̶̗̬̬̰͍̹i͓͉̜͉̠͚͍̬͘͠ͅo̵̠̘̜̟̫̱̟̟͇̕̕n̸̪͖̪̗̕͠


# Contents

## 1. AWS SAM Template Generator

### /aws\_sam\_template_gen
* tasks.py - invoke file

`invoke --help generate-aws-sam-template`

When I first read this, my immediate thoughts were using `invoke` to create a nice CLI for this. It's user friendly, gaining adoption over `fabric`, and developer friendly (win/win). 

It's almost a templating scenario, which I generally reach for jinja -- but this is also a very light use of templates.

I've been using SAM since it debuted, and would recommend using the parameters section of a AWS template to fill in parameters like these (and we could still use a .yml file to store the parameters that we want). But I also wanted to stay close to the assignment.

#### Example invoke:
(from inside the folder with tasks.py)
`inv generate-aws-sam-template -i tests/test_templates/missing-keys.yml -o one-lambda-template.yml`

This grabs the test-template .yml, and outputs a test cloudformation template named one-lambda-template.yml

#### Tests:

(Gherkin tests will follow in a different section)

`python -m pytest`

This will run all of the tests I've written, and explode if I messed anything up.

They're written in pytest, and for the translation, do not need to mock anything with moto. They do not currently run/test with the AWS SAM CLI.

#### AWS SAM CLI:

This assumes your lambda file is already zipped, and you have an event_file.json to send to your lambda (could be a file with only `{}` in it)

* Output a file to template.yml (`inv generate-aws-sam-template -i mytest.yml -o template.yml`)
* run `sam local invoke {Lambda name in template} -e event_file.json` (requires docker)



## 2. ECS Task Lambda
### /execute-ecs-task
* execute-handler.py::execute\_ecs\_event(): the main lambda handler

I currently use quite a few s3 triggers/lambda. Not much ECS, so I'm pretty new to that side of the world.

Mocking S3 objects is something I'm familiar with in Moto, and "I'm sure ECS should be a breeze" was the developer's famous last words. That took me quite awhile (and had to look at the moto tests to figure out what was wrong)

#### Tests:

* execute\_ecs\_task/tests/test\_execute\_handler.py: Mocking s3 is rather straight forward. ECS was a bit of a bother. Again, I'm new to it. But moto seems to have quite a few juicy bugs in it around ecs mocking (like having us-east-1 strings hardcoded into ARNs it creates, etc). 

I'll submit a few issues, the moto folks always need a hand. 

## 3. Gherkin



1. Again, I'm new to gherkin but I'll take a swing at a features in each `/tests` folder.
2. Tests are the last line of truths about what a codebase does or does not do. It doesn't matter how many business documents or product owners swear your product does X, if there's no tests for it your code either currently doesn't do X or will soon stop doing X without someone realizing it. 

## 4. Tools

#### 1. VCS 
VCS is a must in 2018. Just in this very exercise I may have accidentally flubbed a command and deleted a `/tests` folder (which not only killed my finished tests, but also my templates). Thankfully I had a local version committed, and all was fine. A team that speaks fluent git will have no problems juggling a dozen stories, all on different feature branches, and not have an issue merging to master (or merging to whatever branching strategy is agreed on). 

Annoying things about VCS:

* git is cryptic. I started in cvs/svn as most did (back in the olden days), but soon moved to mercurial. It has quirks, but overall was much more friendlier in terms of interacting with it. It has been years since I've touched it, so your mileage may vary.
* new people generally skim an intro to git and think they have it -- then force push a 6 month old branch onto a long running release branch. Branch protection goes a long way with people new to version control.
* There are many different ways to skin the cat of source control. Some people like gitflow, some hate it. Some like feature branches, some hate it. Some like release branches, some hate it. It's really up to the team to decide how best to use VCS to help them achieve their goal. 

#### 2. Docker

Docker is a great way to quickly spin up an environment, in a repeatable manner, without having 30 manual steps. I think at some point, everyone's started at a new company, pulled down the git repos and then... well there's no instructions on how to actually run it. Then you're sent to the last person who installed it (which was over a year ago), and she doesn't really remember, and gives you a few pointers... and...

And this even happens in production. 

Docker also has great benefits in running sandboxed applications next to each other on the same machine. 

There are also very neat scalability benefits with docker swarm (horizontally and vertically scaling containers to meet traffic)

#### 3. Languages in a polyglot world

I currently flip between java/ruby/python. I typically prefer python as it's easy to read, has been widely adopted in my current company, and AWS seems very eager to support it. Based on the strengths of the libraries, I'm also happy to pick up java and ruby as needed.

At home I prefer to touch languages outside of this realm, of which I'm currently digging into golang and Elixir. 

## 5. Testing methodology

#### 1.The right role for QA

To me it depends on the maturity of the product, the speed of the team, the flexibility of the team. I've seen small, nimble teams use minimal QA, and keep quality very high with very thorough unit/integration tests, a small suite of automation tests, and black box/exploratory testing.

I've also seen teams really need the very thorough, slower, more careful process of QA. Because of the extra layers of tests, it's a slower process to refactor or add functionality to the app. And when it's a mission critical app that can't have bugs, it's the right thing to do.

#### 2. Two weeks?!
I'd long for a year, honestly. I've currently been focused on helping my company move to a cloud-based approach (with a focus on observability, quality, modern techniques, etc), and we are months into building a process that works the way we want and need it to (and the end isn't even in sight). There's just so many things to consider: architecture, monitoring, logging, security, access, CI/CD, etc. 

If I only had two weeks, I would focus on CI/CD, code standards, security standards, and make sure that a long-term plan of continuing to improve down the path we need to take happens.

#### 3. Automation.
Things to automate: boring repetitive tasks, production critical tasks (deploying code/building an environment), at the very least a thin layer of end-to-end sanity tests. If the product needs it, a whole suite of smoke/regression tests that run on every build can keep a critical project on track.

It is, however, possible to go overboard with automation -- I've seen a project that had so many layers of unit/integration/automated end-to-end tests that a small change would take the whole team time to slowly integrate it into all aspects of code. And again, some products need that, others need the flexibility to change rapidly. 

Manual testing is still a necessity -- it's rare to not have edge cases that cause grief to automate (maybe it's a system that uses live data that refreshes, etc, and the engineering solution to this is just far too much work) and exploratory testing, even in my current systems that have quite a bit of automated tests, catch the most interesting and impactful bugs.

#### 4. What to test

I'm assuming this product is API based, my gut instantly goes to both security and performance but luckily those are being handled. 

If you're crunched for time, go for the most impact. Maybe there's a certain set of core APIs that sees the most use in the app. It should also be simple to at least cover the happy path for the suite of APIs.

Once that is done, take a look at integration code coverage and either try to improve in the areas that have a lot of error paths/branching paths. 


## 6. Chaos 
#### 1. Why chaos engineers
Some recent outages in my life that would've been caught by a chaos engineer:

* A downstream service went down, cascading throughout the entire system. We were not fault tolerant, and had no circuit breaker logic implemented
* A critical service's config went missing: this also killed its' ability to log the errors that would tell us that it was having problems. We were also only using log data to tell if it was angry.

These are things not caught by real-world testing: we focus too much on the happy path.

#### 2. Traits
* An analytical mind
* The ability to automate chaos experiments
* Understanding the full stack -- from the app tier to the web tier, to the hardware and network setup that keeps it all running

#### 3. Live systems?

Very yes. Obviously you can't just sit around disrupting users from using the system. If it's high impact, it can be done at a low traffic point of day, or on a subsection of traffic. You learn so much more doing it on a live system, and not a test system with 1/1000th the traffic.




