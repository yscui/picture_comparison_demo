import os
import json

inputFile = r"D:\Projects\news-screenshot\input.txt"
outputDir = r"D:\Projects\news-screenshot"

html0 = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>截图对比</title>
    <style>
        html,body {
            height: 100%;
            margin: 0;
            overflow: hidden;
        }
        table {
            border-collapse: collapse;
            border: 2px solid #666;
        }
        h3 {
            margin-bottom: 0;
        }
        tr,td,th {
            border: 1px solid #666;
        }
        img {
            width: calc(50vw - 40px);
        }
        .nav {
            height: 40px;
            background: #eee;
            border-bottom: 1px solid #666;
        }
        #main {
            padding: 0 20px;
            height: calc(100% - 60px);
            overflow-y: scroll;
        }
        #pages {
            display: inline-block;
            padding: 8px;
            border-right: 1px solid #666;
        }
        #list-in-page {
            display: inline-block;
        }
        #list-in-page a {
            margin-left: 10px;
        }
    </style>
    <script src="https://code.jquery.com/jquery-2.2.4.min.js"></script>
    <script>
        const idList = 
'''

html1 = '''
let pageNum = 0;
        const pageCount = Math.ceil(idList.length / 10);

        const fCreateTbl = (id, name) => {
            const dMain = $('#main');
            const dListInPage = $('#list-in-page');
            $('<h3 id="th-' + id + '"></h3>').appendTo(dMain);
            let html = '<table>'
                + '<tr><td><b>[' + id + '] - ' + name + '</b></td></tr>'
                + '<tr><th>线上环境</th><th>测试环境</th></tr>'
                + '<tr>'
                + '<td><img src="img/' + id + '-l.png" alt="l"></td>'
                + '<td><img src="img/' + id + '-r.png" alt="r"></td>'
                + '</tr></table>'
            $(html).appendTo(dMain);
            $('<a href="#th-' + id +'">' + id + '</a>').appendTo(dListInPage);
        }

        const fReload = () => {
            $('#main').empty();
            $('#list-in-page').empty();
            setTimeout(() => {
                for (let i = 0; i < 10; i++) {
                    const id = pageNum * 10 + i;
                    if (id >= idList.length) {
                        break;
                    }
                    fCreateTbl(id, idList[id]);
                }
            });
        }

        $(document).ready(() => {
            const dSelectPage = $('#select-page');
            for (let i = 0; i < pageCount; i++) {
                const start = (i * 10);
                const end = Math.min(i * 10 + 9, idList.length - 1);
                dSelectPage.append('<option value="' + i + '">' + start + ' ~ ' + end +'</option>');
            }
            fReload();
            dSelectPage.change(() => {
                pageNum = parseInt(dSelectPage.find("option:selected").val());
                fReload();
            });
            $('#btn-page-prev').click(() => {
                if (pageNum <= 0) {
                    return;
                }
                pageNum--;
                dSelectPage.val('' + pageNum);
                fReload();
            });
            $('#btn-page-next').click(() => {
                if (pageNum >= pageCount - 1) {
                    return;
                }
                pageNum++;
                dSelectPage.val('' + pageNum);
                fReload();
            });
        });

    </script>
</head>
<body>
    <div class="nav">
        <div id="pages">
            <button id="btn-page-prev">前10个</button>
            <select id="select-page"></select>
            <button id="btn-page-next">后10个</button>
        </div>
        <div id="list-in-page"></div>
    </div>
    <div id="main"></div>
</body>
</html>
'''

if not os.path.exists(outputDir):
    os.makedirs(outputDir)

with open(inputFile) as f:
    lines = f.readlines()
for i in range(len(lines)):
    lines[i] = lines[i].strip()

with open(os.path.join(outputDir, "result.html"), 'w', encoding='utf8') as f:
    f.write(html0)
    f.write(json.dumps(lines))
    f.write(html1)
