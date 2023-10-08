import io
import re
import pandas as pd
from bs4 import BeautifulSoup, ResultSet, Tag
import requests


# Get to one plan to obtain the comments
def get_soup(url, headers, cookies):
    """
    Get a BeautifulSoup object given the URL, headers, and cookies.
    :param url: The target URL to get soup from
    :param headers: Request headers
    :param cookies: Cookies
    :return: BeautifulSoup class object
    """
    res = requests.get(url, headers=headers, cookies=cookies)
    return BeautifulSoup(res.text, "html.parser")


# Getting the second table (all plans)
def get_all_plans(headers, cookies):
    """
    Get a Pandas DataFrame of all plans
    """
    view_all_plans_response = requests.get(
        "https://dmponline.eur.nl/paginable/plans/org_admin/ALL",
        headers=headers,
        cookies=cookies,
    )

    # The response body comes in a JSON string. Get only the HTML.
    view_all_plans_html = view_all_plans_response.json()["html"]
    all_plans_soup = BeautifulSoup(view_all_plans_html, "html.parser")
    all_plans_table = all_plans_soup.find(id="my-plans")

    # Convert the scraped table to pandas
    all_plans_df = pd.read_html(io.StringIO(str(all_plans_table)))[0]

    # Getting the plan IDs
    rows = all_plans_table.find_all("tr")
    # Remove the first row
    rows.pop(0)

    # Getting the list of <a> Tags
    a_tags = [row.find("a") for row in rows]

    # Collect hrefs from the <a> Tags
    plan_hrefs = []
    for a_tag in a_tags:
        if a_tag is not None:
            plan_hrefs.append(a_tag["href"])
        else:
            plan_hrefs.append(None)

    # Get plan id from the relative paths
    all_plans_df["plan_path"] = plan_hrefs
    all_plans_df["plan_id"] = all_plans_df["plan_path"].str.extract("/plans/(\d+)$")

    return all_plans_df


def get_comment_from_row(row_element: BeautifulSoup):
    """
    Get a dictionary of comment data from a <li> row element
    """
    comment_elements = row_element.select(".list-group-item > div > ul > li")
    # If there's not match, return None
    if not comment_elements:
        return None
    # First element is the comment body
    comment_body = comment_elements[0].select_one("div")
    # Second element is comment metadata
    comment_author_span = comment_elements[1].select_one("span")

    out_data = {
        "commented_by": comment_author_span.text.strip(),
        "commented_on": comment_author_span.select_one("time").get("datetime"),
        "comment_body": str(comment_body),
    }

    return out_data


def get_question_divs(plan_number, headers, cookies):
    """
    Get the list of questions from a plan
    """
    # Get the soup
    plan_soup = get_soup(
        "https://dmponline.eur.nl/plans/" + str(plan_number),
        headers=headers,
        cookies=cookies,
    )

    # Get the tag for the "Write Plan" tab
    write_plan_element = plan_soup.select_one(
        "#maincontent > div:nth-child(3) > div > ul > li:nth-child(4) > a"
    )

    # If there's no element, return None
    if write_plan_element is None:
        return None

    # Get to the Write Plan Tab
    write_plan_page = get_soup(
        "https://dmponline.eur.nl" + write_plan_element["href"],
        headers=headers,
        cookies=cookies,
    )

    # Each of the questions is contained in .question-body
    question_divs = write_plan_page.select(".question-body")

    return question_divs


def get_question_comments(question_divs: ResultSet[Tag]):
    """
    Get a list of questions with comments
    """
    if question_divs is None:
        return None
    # Get all questions for one DMP
    questions = []
    for question in question_divs:
        # Get the label for the question
        current_question_label = question.find("label").text
        # Get the comments for the question
        comments_header = question.select("#plan-guidance-tab > ul > li")[-1]
        num_comments_text = re.search("(\d+)", comments_header.select("span")[0].text)
        if num_comments_text:
            num_comments = num_comments_text.group()
        else:
            num_comments = 0
            continue
        # Find the element that contains comment rows
        comment_rows = question.find("div", id=re.compile("^notes-")).select(
            ".panel-body > div > div > div"
        )
        # For each row of comments, get comments
        comments_raw = [get_comment_from_row(row) for row in comment_rows]
        # Filter out the None comments
        comments = [comment for comment in comments_raw if comment is not None]

        # Create an dictionary for each question
        current_question = {
            "question_label": current_question_label,
            "num_comments": num_comments,
            "comments": comments,
        }
        questions.append(current_question)
    return questions


def get_comments_for_plan(plan_number, headers, cookies):
    """
    Get a list of questions with comments for a plan.
    Wrapper for `get_question_divs`
    """
    print(f"Processing plan: {plan_number}")
    question_divs = get_question_divs(plan_number, headers=headers, cookies=cookies)
    return get_question_comments(question_divs)
