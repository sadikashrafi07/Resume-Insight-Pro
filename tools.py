from crewai_tools import ScrapeWebsiteTool, WebsiteSearchTool

# ReactJS Interview Questions Tool
reactjs_tool = ScrapeWebsiteTool(
    url='https://github.com/sudheerj/reactjs-interview-questions/blob/master/README.md',
    name='ReactJS Interview Questions Tool',
    description='Tool to scrape and interact with ReactJS interview questions from the specified GitHub repository.'
)

# Angular Interview Questions Tool
angular_tool = ScrapeWebsiteTool(
    url='https://github.com/sudheerj/angular-interview-questions/blob/master/README.md',
    name='Angular Interview Questions Tool',
    description='Tool to scrape and interact with Angular interview questions from the specified GitHub repository.'
)

# Vue.js Interview Questions Tool
vuejs_tool = ScrapeWebsiteTool(
    url='https://github.com/sudheerj/vuejs-interview-questions/blob/master/README.md',
    name='Vue.js Interview Questions Tool',
    description='Tool to scrape and interact with Vue.js interview questions from the specified GitHub repository.'
)

# JavaScript Interview Questions Tool
javascript_tool = ScrapeWebsiteTool(
    url='https://github.com/ganqqwerty/123-Essential-JavaScript-Interview-Questions/blob/master/README.md',
    name='JavaScript Interview Questions Tool',
    description='Tool to scrape and interact with JavaScript interview questions from the specified GitHub repository.'
)

# Full Stack Developer Interview Questions Tool
fullstack_tool = WebsiteSearchTool(
    url='https://www.geeksforgeeks.org/full-stack-developer-interview-questions-and-answers/',
    name='Full Stack Developer Interview Questions Tool',
    description='Tool to scrape and interact with Full Stack Developer interview questions from GeeksforGeeks.'
)

# Data Science Interview Questions Tool
datascience_tool = WebsiteSearchTool(
    url='https://www.geeksforgeeks.org/data-science-interview-questions-and-answers/',
    name='Data Science Interview Questions Tool',
    description='Tool to scrape and interact with Data Science interview questions from GeeksforGeeks.'
)
