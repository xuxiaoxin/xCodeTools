#!/usr/bin/env python
# -*- coding: utf-8 -*-
# GPLv2

"""
将base语言资源文件合并到其他语言
"""

import sys, os, localizable

format_encoding = 'UTF-8'

class GenString:
    def __init__(self, path, base, dest, filename=None):
        self.path = path
        self.base = base
        self.dest = dest
        if filename == None:
            self.filename = "Main.strings"
        else:
            self.filename = filename;
        
        pass
    
    def gen(self):
        basePath = os.path.join(self.path, self.base + '.lproj', self.filename)
        destPath = os.path.join(self.path, self.dest + '.lproj', self.filename)
        outPath  = os.path.join(self.path, self.dest + '.lproj', self.filename + '.txt')
        
        print 'Loading strings files ...'
        print basePath
        baseLang = localizable.parse_strings(filename = basePath)
        print destPath
        destLang = localizable.parse_strings(filename = destPath)
        print 'Done'
        
        print 'Merging ...',
        
        # 将 base 中新增的 merge 到 destLang
        merged = self._mergeTo(baseLang, destLang)
        
        print 'Done'
        self._generate_strings_file(outPath, merged)
        pass
        
        

    # 从 src 集合向 dest 集合 做 merge
    def _mergeTo(self, src, dest):
        out = []
        for item in src:
            destItem = self._find_in(item['key'], dest)
            if(destItem is None):
                out.append(item)
            else:
                out.append(destItem)
        return out
                
    # 从 src 中查找，并返回第一个            
    def _find_in(self, key, src):
        for item in src:
            if(key == item['key']):
                return item
        return None
        
    
    # 生成新的 strings 文件
    def _generate_strings_file(self, filePath, out):
        #    /* Class = "UILabel"; text = "mail"; ObjectID = "0Ew-k9-4Yr"; */
        #    "0Ew-k9-4Yr.text" = "mail";
        
        fw = open(filePath, 'w+')
        for item in out:
            content = u'\n/*' + item['comment'] + u'*/\n' + u'"' + item['key'] + u'" = "' + item['value'] + u'";\n'
            fw.write(content.encode(format_encoding))
        fw.close();
        return
        
    # end of class GenString
    pass



def usage():
    print "Usage: "+sys.argv[0]+"  <ProjectPath>  <BaseLang>  <DestinationLang>"
    print '*'*40
    print "      ProjectPath XCode Project path"
    print "      Base Lang name aka. en"
    print "      Destination Lang name aka. zh-Hans"
    print '*'*40
    sys.exit(0)
    pass
    
def main():
    
    if len(sys.argv) < 4:
        usage()
        
    project_path = sys.argv[1]
    base_lang = sys.argv[2]
    dest_lang = sys.argv[3]
    
    if len(sys.argv) >= 5:
        strings_filename = sys.argv[4]
    else:
        strings_filename = None
        
    g = GenString(project_path, base_lang, dest_lang, strings_filename);
    g.gen()

    pass

if __name__ == '__main__':
    main()