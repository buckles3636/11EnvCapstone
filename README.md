# 11EnvCapstone
2024 MSU Capstone team #11 Environmental Control.
## Workflow!
When working on some new code...
1. Switch to dev (`git switch dev`) and pull any new changes (`git pull`)
2. Create a feature branch off of `dev` (`git checkout -b <feature_name> dev`)
3. Do some coding with nice, helpul commits

> [NOTE!]
> Run `git push -u origin <feature_name>` for your first push to set the remote as upstream

4. When you are ready to create a pull request, you can do it from the terminal or online: from the terminal, run `gh pr create -B <feature_name> -H dev` create a pull request for your feature into dev. If you are doing it online, make sure that you set *base* to *main*!
5. Eventually someone will review and merge the request?