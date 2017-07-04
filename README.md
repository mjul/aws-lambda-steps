# AWS Lambda Step Functions
This is a demonstration of serverless state machines with AWS Step Functions.

It uses the [Serverless](https://serverless.com) framework for easy deployment.


## Example Data
You can use the example data in the `data` directory to try out the services.

### Shops
For example, you can try out the `upload-shops` function like this:

    serverless invoke -f upload-shops -p data/shops.json
	
The `-p` option specifies a path to a JSON or YAML file holding input
data.

### Sales
You can upload some sales data for the shops like so:

    serverless invoke -f upload-sales -p data/sales_aalborg.json
    serverless invoke -f upload-sales -p data/sales_hobro.json
    serverless invoke -f upload-sales -p data/sales_randers.json
