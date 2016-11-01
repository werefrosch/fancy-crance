var veci = [["#218762", "#635785", "#501187", "#651978", "#707632", "#601874", "#275352", "#477100", "#417352", "#683911"], ["#518248", "#896240", "#671877", "#609981", "#562772", "#174320", "#957402", "#864873", "#632773", "#697920"],["#290866", "#275216", "#844175", "#740940", "#940848", "#993623", "#187924", "#772832", "#689144", "#688720"], ["#605736", "#485466", "#291901", "#821453", "#663088", "#810357", "#975301", "#228504", "#708573", "#851917"], ["#286287", "#326656", "#354101", "#737190", "#925483", "#289776", "#950942", "#450503", "#753495", "#659210"], ["#863067", "#718854", "#787251", "#904636", "#498212", "#121676", "#860671", "#523524", "#896551", "#390720"], ["#826531", "#959848", "#623854", "#286085", "#984690", "#906243", "#404794", "#500964", "#936383", "#562724"], ["#301568", "#337245", "#592740", "#762724", "#880140", "#992542", "#362305", "#234881", "#648847", "#806262"], ["#638824", "#137740", "#907102", "#370143", "#480591", "#987927", "#624676", "#819310", "#655884", "#983831"], ["#446803", "#707634", "#593042", "#507568", "#217358", "#449182", "#291257", "#161798", "#672302", "#322387"], ["#567566", "#518461", "#673158", "#323901", "#300425", "#445725", "#552831", "#756210", "#287741", "#610163"], ["#452464", "#350384", "#130955", "#684146", "#773146", "#659840", "#976955", "#287353", "#170419", "#842582"], ["#604464", "#958582", "#513570", "#443021", "#912755", "#564639", "#932800", "#338111", "#908780", "#896226"], ["#753205", "#799201", "#890933", "#674311", "#170625", "#738912", "#720453", "#170596", "#463132", "#600814"], ["#692508", "#216315", "#940266", "#288518", "#662744", "#902814", "#130899", "#555622", "#966437", "#417343"], ["#777907", "#648451", "#638136", "#987692", "#999268", "#933645", "#976104", "#977862", "#739990", "#522068"], ["#467287", "#148930", "#770255", "#894238", "#892548", "#258543", "#186246", "#496719", "#977573", "#311485"], ["#979299", "#999594", "#805413", "#386070", "#501161", "#791929", "#484585", "#558812", "#656962", "#803389"], ["#893191", "#858505", "#692565", "#844612", "#611763", "#589256", "#488426", "#460734", "#109755", "#758568"], ["#851423", "#806243", "#397426", "#724834", "#663999", "#840834", "#540751", "#894448", "#274284", "#560332"]];

var canvas = document.getElementById("canvas"),
         c = canvas.getContext("2d");
/* daco */
// daco ine
c.font = "17px Georgia";
c.textAlign = "center";

var c_x = 1;
var c_y = 1;
var text = "nic";

var render = function(){
    c.clearRect(0, 0, canvas.width, canvas.height);
    var i, j, x, y,
        width = 20, height = 10;
    for (i = 0; i <= height; i++){
        for (j = 0; j <= width; j++){
            c.fillStyle = veci[j][i];
            c.fillRect(j*canvas.width/20 - canvas.width/20, i*(canvas.height - 20)/10 - (canvas.height - 20)/10, canvas.width/20, canvas.height/10);
            c.fillStyle = "#000000";
            //c.fillText(j +","+ i, j*canvas.width / 20 - 20, i*(canvas.height - 20) / 10 - 10);
        }
    }
    c.fillText("X", c_x*canvas.width / 20 - 20, c_y*(canvas.height - 20) / 10 - 10);
    c.fillText(text, canvas.width / 2, canvas.height - 4);
}


$(document).ready(function() {
    var userName = "Anonymous"
    var socket = io.connect('http://' + document.domain + ':' + location.port);
    socket.on('connect', function() {
        socket.send('User has connected!');
    });

    //receive message
    socket.on('message', function(msg) {
        $("#messages").append('<li>'+msg+'</li>');
        console.log('Received message');
    });

    //receive map
    socket.on('data', function(pole) {
        veci = JSON.parse(pole)
        socket.emit('cursor', c_x, c_y);
    });

    socket.on('text', function(txt) {
        text = txt
    });

    //arrows
    function checkArrowKeys(e){
        var arrs= ['left', 'up', 'right', 'down'],
        key= window.event? event.keyCode: e.keyCode;
        if (key && key>36 && key<41) {
            if (arrs[key-37] == 'down') c_y += 1;
            if (arrs[key-37] == 'up') c_y -= 1;
            if (arrs[key-37] == 'right') c_x += 1;
            if (arrs[key-37] == 'left') c_x -= 1;
        }
    }
    document.onkeydown = checkArrowKeys;

    //namebutton
    $('#namebutton').on('click', function() {
        userName = $('#myName').val()
    });
    $('#myName').on('keyup', function() {
        userName = $('#myName').val()
    });

    //sendbutton
    $('#sendbutton').on('click', function() {
        socket.send($('#myMessage').val())
    });
    $('#myMessage').on('keyup', function() {
        if (event.keyCode==13) {
            socket.send($('#myMessage').val())
            }
    });
});




setInterval(render, 300);