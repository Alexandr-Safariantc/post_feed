<a name="readme-top"></a>
<!-- PROJECT LOGO -->
<div align='center'>
  <a href="https://www.python.org/" target="_blank" rel="noreferrer">
    <img src="https://raw.githubusercontent.com/danielcranney/readme-generator/main/public/icons/skills/python-colored.svg" height="95" alt="Python">
  </a>
  <a>
    <img src="https://cdn.pixabay.com/photo/2016/07/26/05/18/pencil-1542024_1280.png" height="110" alt="Post" hspace="0">
  </a>
  </a>
  <a>
    <img src="https://cdn.pixabay.com/photo/2022/07/14/17/31/desktop-7321676_1280.png" height="100" alt="Blog" hspace=10>
  </a>

<h3 align="center">Post Feed</h3>

  <p align="center">
    Web app to share your breathtaking stories
    <br />
    <a href="#getting-started"><strong>--> Quick start <--</strong></a>
    <br />
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#features">Features</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#Run-as-python-script">Run as python script</a></li>
        <li><a href="#Secrets">Secrets</a></li>
      </ul>
    </li>
    <li><a href="#explanation">Explanations</a></li>
    <li><a href="#restrictions">Restrictions</a></li>
    <li><a href="#contacts">Contact</a></li>
  </ol>
</details>

## Features
- Adding your amazing stories to feed and show them for other users.
- Editing your post if you want to make it perfect.
- Watching other users' posts.
- Adding your posts to thematic groups.

## Built With
![](https://img.shields.io/badge/python-3.9.19-blue)
![](https://img.shields.io/badge/FastAPI-0.110.1-blue)
![](https://img.shields.io/badge/SQLAlchemy-2.0.29-blue)
![](https://img.shields.io/badge/pydantic-2.6.4-blue)
![](https://img.shields.io/badge/alembic-1.11.1-blue)
![](https://img.shields.io/badge/python_jose-3.3.0-blue)
![](https://img.shields.io/badge/sqladmin-0.16.1-blue)
![](https://img.shields.io/badge/click-8.1.7-blue)
![](https://img.shields.io/badge/Pytest-7.1.3-blue)

![](https://img.shields.io/badge/test_coverage-98%25-green)

# Getting Started

## Run as python script
### Prerequisites

* python **3.9.19**
* pip

### Installation

1. Clone the repo
   ```sh
   $ git clone https://github.com/Alexandr-Safariantc/post_feed
   ```
2. Activate virtual environment
   ```sh
   $ cd post_feed
   $ python3 -m venv venv
* for Linux/macOS
    ```sh
    $ source .venv/bin/activate
    ```
* for windows
    ```sh
    $ source .venv/scripts/activate
    ```

3. Upgrade pip
    ```sh
    (venv) $ python3 -m pip install --upgrade pip
    ```

4. Install requirements
    ```sh
    (venv) $ pip install -r requirements.txt
    ```

5. Migrate database
    ```sh
    (venv) $ alembic upgrade head
    ```

6. Add test data to database
    ```sh
    (venv) $ python3 cli.py test-data
    ```

7. Run app
    ```sh
    (venv) $ uvicorn main:app --reload
    ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Secrets

#### .env secrets

`SECRET_KEY`: key for user password encoding.<br>

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Explanation
### Database Structure

  `User` <br>
  Contains creation date, user data.

  `Group` <br>
  Contains creation date, description, slug, title.

  `Post` <br>
  Contains post author, post group, publication date, text, title.

## Restrictions

**1. Groups for superusers** <br>
We know that you have lots of brilliant ideas for thematic post groups but we have to save resources to ensure all your wonderful posts are featured in our feed.

**2. Titles are required** <br>
We really want to meet your expectations so to make it easier and faster to find exciting post you have to add title to your post.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Planned updates

**1. Comments** <br>
We really appreciate your opinion and we want you to have opportunity to express it, so we are going to add a post commenting feature.

**2. Subscriptions** <br>
We know that you have found your favorite authors in our post feed and we want you to receive their posts first, new author subscription feature will help you.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Contacts

**Alexandr Safariants** Backend developer

[![Gmail Badge](https://img.shields.io/badge/-safariantc.aa@gmail.com-c14438?style=flat&logo=Gmail&logoColor=white&link=mailto:safariantc.aa@gmail.com)](mailto:safariantc.aa@gmail.com)<p align='left'>

<p align="right">(<a href="#readme-top">back to top</a>)</p>