cd public


# 初始化
git init

# 设置账号
git config user.name "name"
git config user.email "email"


# 本地切换分支
git branch gh-pages 
git checkout gh-pages 


# 生成静态页面
hexo clean
hexo g


# commit
git add .
git commit -m "$(date) Update from Action"



# 强制上传
git push --force --quiet "https://kengerlwl:${GITHUB_TOKEN}@github.com/kengerlwl/kengerlwl.github.io.git"  gh-pages    
