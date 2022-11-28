
## What are Azure Functions?

Azure Functions is a serverless solution that allows you to write less code, maintain less infrastructure, and save on costs. Instead of worrying about deploying and maintaining servers, the cloud infrastructure provides all the up-to-date resources needed to keep your applications running.

You focus on the code that matters most to you, in the most productive language for you, and Azure Functions handles the rest.

**Supported Languages: C#, Java, JavaScript, PowerShell, or Python, or use a custom handler to use virtually any other language.**

&nbsp;<br>

## What are Durable Functions?

Durable Functions is an extension of Azure Functions that lets you write stateful functions in a serverless compute environment. The extension lets you define stateful workflows by writing orchestrator functions and stateful entities by writing entity functions using the Azure Functions programming model. Behind the scenes, the extension manages state, checkpoints, and restarts for you, allowing you to focus on your business logic.

- Pattern #1: Function chaining
- Pattern #2: Fan out/fan in
- Pattern #3: Async HTTP APIs
- Pattern #4: Monitor
- Pattern #5: Human interaction
- Pattern #6: Aggregator (stateful entities)

&nbsp;<br>


## Form Recognizer Orchestration with Durable Functions
### High-Level Solution Architecture
&nbsp;<br>
![Alt text](assets/HLD.svg "a title")
&nbsp;<br>
&nbsp;<br>
### Application Architecture - Example 1
&nbsp;<br>
![Alt text](assets/App_Exp_Example_1.svg "a title")
&nbsp;<br>
&nbsp;<br>
### Application Architecture - Example 2
&nbsp;<br>
![Alt text](assets/App_Exp_Example_2.svg "a title")
&nbsp;<br>
&nbsp;<br>
### Application Architecture - Example 3
&nbsp;<br>
![Alt text](assets/App_Exp_Example_3.svg "a title")
&nbsp;<br>
&nbsp;<br>
## Workflow
### Workflow - Single Document
&nbsp;<br>
![Alt text](assets/Workflow_Single_Document.svg "a title")
&nbsp;<br>
&nbsp;<br>
### Workflow - Multiple Documents
&nbsp;<br>
![Alt text](assets/Workflow_Multiple_Documents.svg "a title")
&nbsp;<br>

## Network Architecture
&nbsp;<br>
![Alt text](assets/Network.svg "a title")
&nbsp;<br>
