# Index-All-In-One: A Personal Unified Search Tool

## Project Description
Digital properties of a person include disk files, notes, photos and chat history in cloud applications, etc. Such fragmentation causes problems when it comes to search. People need to use native searches in different applications, which is a waste of time and makes people distracted. Unifying the searches on all personal information like files, notes, codes, etc. can save time and keep the user focused on their real needs.

For privacy concerns, we need an open source unified search framework that can be self hosted either on a local PC or trusted server. Furthermore, trade-offs and optimizations are required for such a framework to run smoothly on personal PCs or normal servers.

The market lacks such an open source unified search framework at this time. Our goal is to develop an app that enables users to easily locate their files across multiple platforms while ensuring their privacy is safeguarded.


## State of the Art

Current solutions such as Elastic Workplace Search, Coveo’s unified search, Apple’s Spotlight, and Watson are either targeting business use only and/or not open source. For privacy concerns, we would like to create an open source framework for personal use.

## Project Approach

Components:
Search engine: The core component of our backend, which is responsible for building, searching and updating the unified index.
Application integration plugins: The component that connects the search engine with other platforms such as email, Google Drive, Notion by sending updates to the backend.
Frontend: The UI where users perform searches and view results.

Technologies:
OpenSearch for search engine, Flutter for frontend UI, Python for integration plugins.

Expected project Outcome:
An app with a unified search framework suitable for running on home devices, integrating files and content from different sources to build and update an index.

## Run in docker compose

Make sure you have `flutter` installed.

Run this command on project’s root dir to start docker compose in detached mode:

```bash
./scripts/run-docker-compose.sh
```

And then access flutter web at localhost:8000.

Or set `SERVER_URL` and `LOCAL_ADDR` in env to run it in different port or remote server.

You can check logs with this command:

```bash
docker-compose -f docker-compose/docker-compose.yml logs --follow
```
