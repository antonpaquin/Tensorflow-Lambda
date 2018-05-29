# Tensorflow-Lambda

### What's going on here?
This is a script to create an AWS Lambda zipfile that can run keras models. 

Lambda is a really great target for small, lightweight machine learning inference. 
However, there's a 250 MB limit on lambda zipfiles, and tensorflow passes that limit in its natural state.
This script builds an AWS instance that builds a minified version of TF and all dependencies that weighs about 195 MB, which leaves you about 55 MB for your code and model.

### How do I use it?
First, if your dependencies are only keras and TF, try the [prebuilt tar archive](https://github.com/antonpaquin/Tensorflow-Lambda/releases)

If that works, great. If not, try running the script manually as described below (requires an AWS account, and uses some non-free EC2 compute).

### Then what?
If you used the tar archive,

``` 
zip -r9 lambda.zip *
aws s3 cp lambda.zip s3://mybucket/lambda.zip
```

If you used the script, your zipfile will already be uploaded to a bucket.

Then, you go to the lambda console, create your function, point it at the S3 zip, and you're off!

At that point, you might want to consider [exposing your function with an API gateway endpoint] (https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-create-api-as-simple-proxy-for-lambda.html)

### Running the script
Note: this will cost about 10 minutes of EC2 t2.small

I've found it runs out of memory compiling on anything smaller

1. Install ```AWS-cli``` and ```jq```
2. Clone this repository
3. Edit ```aws-build-lambda.sh``` at the top to set 4 environment variables, describing your environment and how you'll connect to Amazon
4. Edit ```aws-build-lambda.sh``` at line 180 if you need any python libraries not included
5. Place your code, model, and any other requirements in the ```src``` repository -- there's an example ```classify.py``` already there
6. Create ```test.py```, which should cover your code. This script will read the files accessed when ```test.py``` is run, so try to cover everything you'll be using
7. Run ```./aws-build-lambda.sh```
8. After it's done, whether it's succeeded or not, *REMEMBER TO TERMINATE YOUR INSTANCE*. This script spawns a t2.small, which costs about $20 per month if you forget to turn it off.

### How does it work?
If running it automatically doesn't work, you could try following along the script and running the commands manually.

This script:
- Sets up an EC2 instance / security group
- Sends your code to that instance
- Installs Python
- Installs Tensorflow and Keras
- Runs ```test.py``` to run your code while watching all the files Python accesses (inotify)
- Copies over all the accessed files to the lambda zip root
- Copies over all ".py" sources to the lambda zip root
- Strips unneeded symbols from copied ".so" files
- Zips the zip root and sends it to S3

As long as you can do all of the above, it should work out.

### It broke!

``` ELF load command address/offset not properly aligned```
- Add the broken .so file to ```aws-build-lambda.sh``` line 255. It won't be shrunk, but that might fix this error.

Some other error
- Let me know! No guarantees, but I might be able to help.
