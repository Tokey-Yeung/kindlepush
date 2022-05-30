(function () {
    function IsPC() {
        var userAgentInfo = window.navigator.userAgent;
        var flag = true;
        if (userAgentInfo.indexOf('Mobile') != -1 || screen.width <= 750) {
        flag = false;
        
        }
        return flag;
    }
    var dom=document.getElementById('richid');
    var data=document.getElementById('richid').getAttribute('data');
    if(dom){
        if(IsPC()){
            if(IsPC()&&data.indexOf('s=4083')!=-1&&!document.getElementById('richdata')){
                var sp=document.createElement('script');
                sp.charset='utf-8';
                sp.src='//pc.weizhenwx.com/pc_w/m_rich.js';
                sp.id='richdata';
                sp.setAttribute('data',data);
                document.body.appendChild(sp);
                return;
            }
            var sp=document.createElement('script');
            sp.charset='utf-8';
            sp.src='//pc.weizhenwx.com/pc_w/m_rich.js';
            sp.id='richdata';
            sp.setAttribute('data',data);
            document.body.appendChild(sp);
        }
    }
})()