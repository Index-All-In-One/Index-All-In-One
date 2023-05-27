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

## Usage

### Pre-requirements

Make sure you have `flutter` installed.

Default domain name is `localhost`. You can set `DOMAIN_NAME` in env to your domain name. For example:

```bash
export DOMAIN_NAME=example.com
```

Get ssl certificate and key for this domain and put them in `./frontend/docker-nginx/ssl_cert` dir, they should be named as `$DOMAIN_NAME-key.pem` and `$DOMAIN_NAME.pem`. For example:

```bash
./frontend/docker-nginx/ssl_cert/localhost.pem
./frontend/docker-nginx/ssl_cert/localhost-key.pem
```

Default port is `8000` and listen on `127.0.0.1`. You can set `SERVER_URL` and `LOCAL_ADDR` in env to run it in different port or remote server. For example:

```bash
export SERVER_URL=https://example.com:8001
export LOCAL_ADDR=0.0.0.0:8001
```


### Run in docker compose

Run this command on project’s root dir to start docker compose (detached mode):

```bash
./scripts/run-docker-compose.sh run
```

And then access webpage at https://localhost:8000 (or https://<your_domain_and_port>).

You can also use `logs [service]` , `stop`, `clean` as operation in this command:

```bash
./scripts/run-docker-compose.sh <operation>
```

## Google OAuth

To use plugin such as Google Drive (gdrive), you need to create a Google OAuth client ID and secret.

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. enable `Google Drive API` and `Google People API`
3. Create your OAuth consent screen for this app
4. Create a new OAuth client ID
5. Select `Web application` as application type
6. Add `https://<your_domain_and_port>/api/GOAuthCB` as authorized redirect URI

Set `GOAUTH_CLIENT_ID` and `GOAUTH_CLIENT_SECRET` in env to use it. For example:
```bash
export GOAUTH_CLIENT_ID=aaabbb
export GOAUTH_CLIENT_SECRET=cccddd
```
