# AWS Lambda Step Functions
This is a demonstration of serverless state machines with AWS Step Functions.

It uses the [Serverless](https://serverless.com) framework for easy deployment.

Make sure the plugins are installed (`npm install`) and then run `serverless deploy`
to deploy the project.

# Step Functions
The project defines Step Functions composed of Lambda Functions.
The Step Functions are exposed over HTTPS.

The Step Functions can be executed like so (you need to substitute the correct URL)

    curl -XPOST https://SOMEPREFIX.execute-api.eu-central-1.amazonaws.com/dev/sales/upload -d  @data/sales_aalborg.json


# Lambda Functions
You can use the example data in the `data` directory to try out the services.

## Shops
### `upload-shops`
For example, you can try out the `upload-shops` function like this:

    serverless invoke -f upload-shops -p data/shops.json
	
The `-p` option specifies a path to a JSON or YAML file holding input
data.

### `list-shops`
Get the list of all shops.

    serverless invoke -f list-shops

## Sales

### `upload-sales`
You can upload some sales data for the shops like so:

    serverless invoke -f upload-sales -p data/sales_aalborg.json
    serverless invoke -f upload-sales -p data/sales_hobro.json
    serverless invoke -f upload-sales -p data/sales_randers.json

### `generate-weekly-sales-report`
This generates the weekly sales report for one shop for one week.
You must specify the `date` for the report and the `shopNumber`.

    serverless invoke -f generate-weekly-sales-report --data '{"date":"2017-07-12", "shopNumber": 1}'

