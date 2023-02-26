hexo clean
hexo g
cd public

git init

git config --global user.name “kengerlwl”
git config --global user.email "kengerlwl@qq.com"


git add .
git commit -m "$(date) Update from Action"


git push --force --quiet "https://kengerlwl:${GITHUB_TOKEN}@github.com/kengerlwl/kengerlwl.github.io.git"  gh-pages    
