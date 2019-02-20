var exec = require('child_process').exec;

var refresh = function () {
	
	exec('python crawler.py', function(error,stdout,stderr){
    	if(stdout.length > 0){
        	console.log(stdout);
    	} 
    	if(error) {
        	console.info('stderr : '+stderr);
    	}
	});
}

const time = setInterval(() => {
	console.log('Refresh the MongoDB.');
	var time=new Date().toLocaleString();
	console.log(time);
	refresh();
}, 30*60000); // 10min