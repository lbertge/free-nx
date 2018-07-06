# free-nx

This is mostly an exercise in learning about different technologies (AWS Lambda, Serverless, BeautifulSoup), and how to correctly use a web browser's debugging tools (examining REST request information, such as header info, status, and inspecting the DOM)

The premise of this project is pretty stupid; I've noticed that, in some private
servers, the CAPTCHA verification isn't actually required for the vote to be
validated. What this means is that you could write a bot to automate the
clicked links, and reap the rewards without human verification. This basically
allows one to passively generate in-game currency without having to log in every
XX hours.

I've tried to make the code generalizable, so if you wish to modify it for your own purposes, here's a brief recap of what I did:

This repo requires the BeautifulSoup and requests modules, and is built for Python 3. To install these into the local directory, run

```
pip3 install bs4 requests -t ./scraper/
```

The core of the code is in `scraper/handler.py`, in the `method()` function. I'm
using AWS Lambda here to deploy this function, and have a `cron` job which
executes every XX hours; but setting up a cron job on your own computer is not
that hard, and is practically easier than the overhead of managing
users/permissions on the AWS console.

Your credentials/target URL are specified in the file `scraper/data/example.json`. I've currently created four fields that you may have to change:
```
username*: yourusername (please read the bolded note below)
password*: your password (please read the bolded note below)
loginPage*: a POST request, which usually contains the URL of the webpage with the login form. (please read the bolded note below)
postLogin[]: an list of the pages you want to crawl after successfully logging into a page
```

__*A word about username/password/login:__ 
You likely will have to change the field title. To figure this out, inspect the DOM, and look for the `name` attribute for the username/password input fields. This is how the `requests` module determines where to place your supplied username and password payload.
A similar rule applies for loginPage. Sometimes it's not immediately obvious what the POST URL is. What you can do is go to your browser's inspector, and click on Network. If you manually click the 'Login' button, the browser should log a POST request, along with all relevant request information. That POST request's URL is what you want.

I'm also using serverless to help automatically upload the packaged function
onto AWS. To do what I did, set up your serverless credentials, visit [the AWS guide](https://serverless.com/framework/docs/providers/aws/guide/credentials/?utm_source=cli&utm_medium=cli&utm_campaign=cli_helper_links)
Since we're specifying a package for serverless to upload, you can create a zipped package for it by running

```
cd scraper/
zip -r package.zip *
```

Then in this root directory, run 

```serverless deploy```

and you should be able to visit your AWS Lambda Management Console to verify the
code has been uploaded.

Finally, AWS has a CloudWatch service that you can use to time a cron job, which
you can link up with your Lambda function.

Happy farming!

### Acknowledgements

Thanks to @kagemusha's [scraping tutorial with AWS Lambda](https://medium.com/@kagemusha_/scraping-on-a-schedule-with-aws-lambda-and-cloudwatch-caf65bc38848) for guidance.
