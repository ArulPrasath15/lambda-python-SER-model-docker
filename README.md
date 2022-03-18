# Jovi SER Model Container

## Building Docker Image

```
λ docker build -t lambda-jovi-ser
```

## Running the Container

```
λ docker run -p 8080:8080 lambda-jovi-ser
```

## Invoking the Function

```
λ curl -XPOST "http://localhost:8080/2015-03-31/functions/function/invocations" -d "{"""msg""":"""hello"""}"
```

## Requirements

* **numpy**: 1.21.2
* **boto3**: 1.20.37
* **tensorflow**: 2.2.0
* **librosa**: 0.8.1
* **keras**: 2.7.0
* **scikit-learn**: 0.24.2

<hr>

## References
1. [Deploying Docker in Lambda](https://levelup.gitconnected.com/deploying-aws-lambda-with-docker-containers-i-gave-it-a-try-and-heres-my-review-147327519ce9)
2. [Lambda Python in ECS](https://towardsdatascience.com/aws-lambda-with-custom-docker-images-as-runtime-9645b7baeb6f)
