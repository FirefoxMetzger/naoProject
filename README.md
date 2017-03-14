# naoProject
A repository holding data for the NAO Project in AINT512 with Plymouth University

Any part of the software can be considered unstable and is subject to change until it reaches version 1.0.0.

# Versioning

Versions are tracked using: MAJOR.MINOR.PATCH

See: http://semver.org/

# Contribution

We are using a standard centralized gitflow: master-development-feature-patch
Releases are branched of master (name: vMAJOR-MINOR i.e. v1-0). Bugfixes are added to these branches and tagged (name: vMAJOR-MINOR-PATCH i.e. v1-0-5)

New versions are created by merging all features from development into master.

## Adding new Features using a feature branch:

1) Create a feature branch (assuming your remote is called origin):
```
git checkout master
git pull origin
git checkout -b <feature-name>
git push -u origin <feature-name>
```
   
Explaination: the first command checks out the master branch and the second one updates it. Then we create a new branch ('-b') named after the feature to be implemented and switch to that branch. Next we create the branch on the remote repository and tell get we wish to keep it 'in sync' ('-u') with ours.
    
2) Write your changes and do what you have to do. Remember to commit regulary!
3) When done submit a pull request (see below) to the development branch

## Adding a bugfix using a patch branch:

1) Create a bugfix/patch branch (assuming your remote is called origin):

    git checkout master
    git pull origin
    git checkout -b <bug-name>-<issue-number>
    git push -u origin <bug-name>-<issue-number>
    
    For explaination of the commands, see above
    
2) Write the fix.
3) Submit a pull request to to the version in which the fix occurred.
4) Once integrated, we will propagate the fix through all versions until it reaches master

## Create a new pull request (PR) for revision:
	- Go to
	
	    https://github.com/FirefoxMetzger/naoProject/pulls
	    
	and click "New Pull Request"
	- select the branch you want to add the commits (base)
	- select the branch you want to pull from (compare)
	- click create pull request and write a few lines about the code you wish to add
	
	
