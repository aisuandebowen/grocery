# grocery
My grocery

## nbconvert修改图片路径

## 命令
```
jupyter nbconvert mynotebook.ipynb --to markdown --template=nbconvert_imgPath_template --TemplateExporter.extra_template_basedirs=. --NbConvertApp.output_files_dir="markdown-img/{notebook_name}.assets"
```
