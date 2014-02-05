__author__ = 'mandrake'

from flask import Blueprint, render_template, Response, send_from_directory
import base64

routes = Blueprint('index', __name__, template_folder='templates', static_folder='static')
prefix = ''
#static_path = 'static/main'


@routes.route('/')
def root():
    return render_template('index.html')


@routes.route('/favicon.ico')
def favicon():
    return Response(
        base64.decodestring('AAABAAEAICAAAAEAIACoEAAAFgAAACgAAAAgAAAAQAAAAAEAIAAAAAAAABAAABILAAASCwAAAAAAAAAAAAD/NRH\
        //zgT//87FP//PxX//0EW//9EF///Rxf//0oY//9MGf//Txr//1Eb//9TG///VRz//1cd//9ZHf//Wx7//1we//9dH///Xx///18f//9gIP/\
        /YSD//2Eg//9hIP//YiD//2Eg//9hIP//YCD//2Ag//9fH///Xh///1wf//84E///OxT//z8V//9CFv//RRf//0gY//9LGf//TRr//1Aa//9\
        SG///VRz/91Qc/99NGf/fUBr/31Eb/99TG//fVBz/31Uc/99WHP/fVxz/31gd//9lIf//ZiL//2Yi//9mIv//ZiL//2Yi//9lIf//ZCH//2M\
        h//9iIP//YSD//zsU//8/Ff//Qhb//0UX//9IGP//Sxn//04a//9RG///Uxz//1Yc//9ZHf//Wx7/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD\
        /AAAA/wAAAP//aSP//2oj//9rI///ayP//2sj//9rI///aiP//2kj//9oI///aCL//2ci//9lIf//PxX//0IW//9FF///SBj//0sZ//9PGv/\
        /URv//1Qc//9XHf//Wh7//1wf//9fH/9zKw7/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA//9uJP//byT//28k//9vJf//byX//28l//9\
        vJP//biT//20k//9sJP//ayP//2kj//9BFv//RRf//0gY//9LGf//Txr//1Ib//9VHP//WB3//1se//9eH///YCD//2Mh//9lIf8AAAD/AAA\
        A/wAAAP8AAAD/AAAA/wAAAP9HHwr//3Im//9zJv//cyb//3Qm//90Jv//cyb//3Mm//9zJv//cib//3Al//9vJf//biT//0QX//9IGP//Sxn\
        //08a//9SG///VRz//1gd//9bHv//Xh///2Eg//9kIf//ZyL//2kj/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/4c+Ff//dyf//3cn//94KP/\
        /eCj//3go//94KP//dyf//3cn//92J///dSf//3Mm//9yJv//Rxf//0sZ//9OGv//Uhv//1Uc//9YHf//Wx7//18f//9iIP//ZSH//2ci//9\
        qI///bST/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/u1kd//97Kf//fCn//3wp//99Kf//fSn//3wp//98Kf//eyn//3so//95KP//eCj//3Y\
        n//9KGP//TRr//1Eb//9VHP//WB3//1se//9fH///YiD//2Uh//9oI///ayP//24k//9xJf8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP+/Xx/\
        //38q//+AK///gSv//4Er//+BK///gSv//4Ar//+AKv//fyr//34q//98Kf//eyj//0wZ//9QG///VBz//1cd//9bHv//Xh///2Ig//9lIf/\
        /aCP//2sk//9vJf//cSb//3Qn/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/79iIP//hCz//4Us//+FLP//hiz//4Ys//+GLP//hSz//4Qs//+\
        DK///giv//4Aq//9/Kv//Txr//1Mb//9WHP//Wh7//14f//9hIP//ZSH//2gj//9rJP//byX//3Im//91J///eCj/AAAA/wAAAP8AAAD/AAA\
        A/wAAAP8AAAD/v2Uh//+ILf//iS3//4ou//+LLv//iy7//4ou//+KLv//iS3//4ct//+GLP//hCz//4Mr//9RG///VRz//1kd//9dH///YCD\
        //2Qh//9nIv//ayP//28l//9yJv//dSf//3go//97Kf8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP+/aCL//40v//+OL///jy///48v//+PL//\
        /jy///44v//+NL///jC7//4su//+ILf//hyz//1Mc//9XHf//Wx7//18f//9jIf//ZyL//2oj//9uJP//cSb//3Un//94KP//eyn//38q/wA\
        AAP8AAAD/AAAA/wAAAP8AAAD/AAAA/79rJP//kTD//5Iw//+TMf//kzH//5Mx//+TMf//kzD//5Iw//+QMP//jy///40v//+LLv//VRz//1k\
        e//9dH///YSD//2Uh//9pI///bST//3El//90J///eCj//3sp//9/Kv//giv/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/n1we//+VMv//lzL\
        //5cy//+YMv//mDL//5gy//+XMv//ljL//5Qx//+TMP//kTD//48v//9XHf//Wx7//18g//9jIf//ZyL//2sk//9vJf//cyb//3cn//97Kf/\
        /fir//4Ir//+FLP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP9/TBn//5oz//+bM///nDT//5w0//+cNP//nDT//5sz//+bM///mDP//5cy//+\
        UMf//kjD//1kd//9dH///YSD//2Ui//9pI///biT//3Im//91J///eSj//30p//+BK///hSz//4gt/x8RBf8AAAD/AAAA/wAAAP8AAAD/AAA\
        A/186E///njT//581//+gNf//oTX//6E1//+hNf//oDX//580//+dNP//mzP//5gz//+WMv//Wx7//18f//9jIf//ZyL//2sk//9vJf//dCb\
        //3go//97Kf//fyr//4Ms//+HLf//iy7/PyML/wAAAP8AAAD/AAAA/wAAAP8AAAD/HxQG//+iNv//pDb//6U3//+lN///pjf//6U3//+kNv/\
        /ozb//6E1//+fNP//nDT//5kz//9cH///YCD//2Uh//9pI///bST//3Em//91J///eij//34q//+CK///hiz//4ou//+NL/8/JAz/AAAA/wA\
        AAP8AAAD/AAAA/wAAAP8AAAD//6c3//+oOP//qTj//6o4//+rOP//qjj//6g4//+nN///pTf//6M2//+gNf//nDT//10f//9iIP//ZiL//2s\
        j//9vJf//cyb//3co//97Kf//fyr//4Qs//+ILf//jC7//5Aw/xsQBf8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP//qzj//6w5//+uOv//rzr\
        //686//+uOv//rTn//6s5//+pOP//pjf//6M2//+gNf//Xx///2Mh//9nIv//bCT//3Al//90J///eSj//30p//+BK///hSz//4ou//+OL//\
        /kjD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA//+uOv//sTv//7I7//+zO///szv//7M7//+xO///rzr//6w5//+pOP//pzf//6M2//9\
        fIP//ZCH//2gj//9tJP//cSX//3Yn//96KP//fyr//4Mr//+HLf//iy7//48w//+UMf8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD//7I\
        7//+1PP//tzz//7g9//+4Pf//tz3//7U8//+zO///sDr//605//+pOP//pTf//2Ag//9lIf//aSP//24k//9yJv//dyf//3sp//9/Kv//hCz\
        //4gt//+ML///kTD//5Ux/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP//tTz//7g9//+7Pv//vD7//7w///+7Pv//uT3//7Y8//+zO//\
        /sDr//6w5//+oOP//YSD//2Uh//9qI///biT//3Mm//93KP//fCn//4Ar//+FLP//iS3//44v//+SMP//lzL//5sz//+fNf//ozb//6g4//+\
        sOf//sDv//7Q8//+4Pf//vD7//78////BQP//wUD//8BA//+9P///uj3//7Y8//+yO///rjr//6k4//9hIP//ZiL//2sj//9vJf//cyb//3g\
        o//98Kf//gSv//4Us//+KLv//ji///5Mx//+XMv//mzT//6A1//+lN///qTj//606//+yO///tjz//7s+//+/P///wkD//8VB///FQf//xEH\
        //8BA//+8Pv//uD3//7Q8//+vOv//qzn//2Eg//9mIv//ayP//28l//9zJv//eCj//3wp//+BK///hSz//4ou//+PL///kzH//5cy//+cNP/\
        /oDX//6U3//+pOP//rjr//7M7//+3Pf//uz7//8BA///FQf//zET//8xE///GQv//wkD//74///+4Pf//tDz//7A6//+rOf//YSD//2Yi//9\
        rI///byX//3Mm//94KP//fCn//4Er//+FLP//ii7//48v//+TMf//lzL//5w0/wcFAf8AAAD/AAAA/wAAAP8AAAD//7c9//+7Pv//wED//8V\
        B///MRP//zET//8ZC///CQP//vj///7k9//+0PP//sDr//6s5//9hIP//ZiL//2sj//9vJf//cyb//3go//98Kf//gSv//4Us//+KLv//ji/\
        //5Mx//+XMv8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD//7s+//+/P///wkH//8VB///FQf//xEH//8FA//+8Pv//uD3//7Q8//+vOv/\
        /qzn//2Eg//9lIf//aiP//24l//9zJv//dyj//3wp//+AK///hSz//4kt//+OL///kjD//5cy/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wA\
        AAP8/Lg///7s+//+/P///wUD//8FA///AQP//vT///7o9//+2PP//sjv//646//+pOP//YCD//2Uh//9pI///biT//3Im//93J///eyn//38\
        q//+ELP//iC3//4wv//+RMP//lTH/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/3dVHP//uD3//7s+//+8P///vT///7s+//+5Pf//tjz\
        //7Q8//+wOv//rDn//6g4//9fIP//ZCH//2gj//9tJP//cSX//3Yn//96KP//fyr//4Mr//+HLf//iy7//48w//+UMf8AAAD/AAAA/wAAAP8\
        AAAD/AAAA/wAAAP8AAAD//7I7//+1PP//tj3//7g9//+4Pf//tz3//7U8//+zPP//sDv//605//+pOP//pTf//18f//9jIf//ZyL//2wk//9\
        wJf//dCf//3ko//99Kf//gSv//4Us//+KLv//ji///5Iw//+WMv/bhCz/AAAA/wAAAP8AAAD/g1Yd//+rOf//rjr//7E7//+yO///szz//7M\
        8//+yO///sTv//686//+tOf//qTj//6c3//+jNv//XR///2Ig//9mIv//ayP//28l//9zJv//dyj//3sp//9/Kv//gyz//4gt//+ML///kDD\
        //5Mx//+XMv//mzT//581//+iNv//pTf//6g4//+qOf//rDn//646//+uOv//rjr//646//+tOf//qzn//6k4//+mN///pDb//6A1//9cH//\
        /YCD//2Uh//9pI///bST//3Em//91J///eij//34q//+CK///hiz//4ou//+NL///kTD//5Ux//+YM///mzT//581//+hNv//pDf//6Y3//+\
        oOP//qTj//6o4//+qOf//qjj//6k4//+nOP//pTf//6M2//+gNf//nTT/AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\
        AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\
        AAAAAAAAAAAA='),
        mimetype='image/png'
    )


@routes.route('/login', methods=["GET", "POST"])
def login():
    pass


@routes.route('/logout')
def logout():
    return "any"
    pass

'''
@routes.route('/static/<path:path>')
def static(path):
    print static_path, path
    return static_path
    return send_from_directory(static_path, path)'''