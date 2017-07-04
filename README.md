
## Example Data
You can use the example data in the `data` directory to try out the services.
For example, you can try out the `upload-shops` function like this:

    serverless invoke -f upload-shops -p data/shops.json
	
The `-p` option specifies a path to a JSON or YAML file holding input
data.

