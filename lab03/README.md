
# Lab 3

#Team Members
Jessica Awad: 2939433007
Matillda Awad: 4518997700

# Questions 1-4 Answers
Question 1: Why are RESTful APIs scalable?
Based on the link provided (Amazon Web Service), they are scalable because REST optimizes client-server communication by avoiding server overload through statelessness (server doesn’t have to store past request context) and eliminating some client-server interactions through caching.
Question 2: According to the definition of “resources” provided in the AWS article above, what are the resources the mail server is providing to clients?
AWS defines “resources” as “information that different applications provide to their clients.” For example, text data or numbers. In particular to this lab, the mail server provides the recipient name, sender name, subject, and body of text to the mail client. In addition, it can be a user inbox or sent mailbox.
Question 3: What is one common REST Method not used in our mail server? How could we extend our mail server to use this method?
Based on AWS, the four common HTTP methods are: GET, POST, PUT and DELETE. In our mail server, we don’t use PUT which provides the client the ability to update data in a resource. For our mail server, we add it with the endpoint PUT /mail/<mail_id> to modify message (in Flask: @app.route('/mail/<mail_id>', methods=['PUT'])).
Question 4: Why are API keys used for many RESTful APIs? What purpose
do they serve?
Based on AWS, API Keys are used for authentication tokens as it allows the server to assign a unique value to a first-time client, which the client will then use to verify itself every time it wants to access resources. This would prove that you are authorized to make requests to the API. They give developers a set of access rights for certain features or data of an application.
