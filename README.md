Project Description
Motivation/Background
(Describe the problem you want to solve and why it is important. Max 300 words).
Digital properties of a person include disk files, notes, photos and chat history in cloud applications, etc. Such fragmentation causes problems when it comes to search. People need to use native searches in different applications, which is a waste of time and makes people distracted. Unifying the searches on all personal information like files, notes, codes, etc. can save time and keep the user focused on their real needs.

For privacy concerns, we need an open source unified search framework that can be self hosted either on a local PC or trusted server. Furthermore, trade-offs and optimizations are required for such a framework to run smoothly on personal PCs or normal servers.

The market lacks such an open source unified search framework at this time. Our goal is to develop an app that enables users to easily locate their files across multiple platforms while ensuring their privacy is safeguarded.


State of the Art / Current solution
(Describe how the problem is solved today (if it is), and the innovation/advance of your project. Max 200 words).
Current solutions such as Elastic Workplace Search, Coveo’s unified search, Apple’s Spotlight, and Watson are either targeting business use only and/or not open source. For privacy concerns, we would like to create an open source framework for personal use.

Project Approach
(Describe how do you plan to articulate and design a solution, including platform and technologies to use. Include initial milestones as well. Max 300 words).
Components: 
Search engine: The core component of our backend, which is responsible for building, searching and updating the unified index.
Application integration plugins: The component that connects the search engine with other platforms such as email, Google Drive, Notion by sending updates to the backend.
Frontend: The UI where users perform searches and view results.

Technologies:
Elasticsearch for search engine, Flutter for frontend UI, Python for integration plugins.

Milestones:
The backend is able to build indexes, put in dummy data and perform a search.
The backend is capable of updating content, ready to receive information from plugins.
One plugin connected with the backend, able to send info.
A minimum viable product with a frontend, able to perform a search on a platform.
Add support for image search.
Add more plugins.
A completely tested product, like Apple's Spotlight, that is self-hosted and has useful plugins for integrating with other applications.


Project Outcome / Deliverables
(Describe what are the outcomes of the project and how you will conduct a short final demo. Max 200 words).
Outcome:
An app with a unified search framework suitable for running on home devices, integrating files and content from different sources to build and update an index.

Demo:
Connect applications such as Gmail, Google drive, etc to the search engine, and perform unified searches on frontend UI.

