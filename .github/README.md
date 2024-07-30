# Pipeline Catalogue


## Build documentation

We use Yack to build and publish the documentation for this catalogue, so if you don't have installed 
 **adv**  on your system, you can  run the ```make doc-install-adv``` command. 
 
 After that, you need to enable the Yack webhook on your repo. You can do that using one of the following methods:

- Run ```adv yack webhook --enable``` or
- Check the ADV documentation [here](https://github.mpi-internal.com/spt-DevRel/yack-user-guide/blob/master/getting-started/webhook.md): 


Your documentation should be updated using the **_docs** folder, which is the one containing the MarkDown files. After that, you will need to build it with the ```make doc-build``` command and push the **docs** folder into your github repository

To view your doc locally, just run the following command from the root folder:

- ```make doc-view```:  This command will start a server with your rendered documentation

