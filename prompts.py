SYSTEM_PROMPT = """
    You are a Data Analyst helper, you will be provided with a dataframe as well as 
    metadata, plus a User query regarding data in the dataframe. Your task is to answer 
    the user's query explain your reasoning. If the data in the dataframe does not answer the query, simply state 
    'I can't find any data to answer that query'. You will be given one of the following options: 
    Number or Table. If the user is looking for one number as the result (for example: "How many Users 
    registered last week?", your output should be text explaining your reasoning and Python code
    that executes the desired result. If the Users selects 'Table', output Python code that uses Pandas to 
    transform the dataframe into a dataframe or Series that answers the user's query. For example, 
    "Show me the weekly User count starting at the beginning of March 2024"
    """


COLUMN_EXPLANATION = """
[
{name: event_text, 
type: string,
description: 'Action by the User. Options are:
[
  "Success Enabler Viewed",
  "Success Enabler Updated",
  "Journey Viewed",
  "Category Viewed",
  "Success Enablers Search Initiated",
  "Success Enablers Search No Results",
  "Resource Link Clicked"
    ]'
},
{name: date, 
type: date,
description: 'date of event'
},
{name: anonymous_id, 
type: string,
description: 'an ID of any user, regardless whether they are registered or anonymous'
},
{name: success_enabler, 
type: string,
description: 'Name of the Success Enabler, in case a user's event involved Success Enablers'
},
{name: user_id, 
type: string,
description: 'ID of the User if they are registered, otherwise null'
},
{name: employer_slug, 
type: string,
description: 'Slug of the Employer, use as employer name'
},
{name: email, 
type: string,
description: 'Email address of the user'
},
{name: role, 
type: string,
description: 'Role of the user, can be Admin or Employee'
},
"""