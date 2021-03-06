module.exports = function(grunt) {
    grunt.initConfig({
        less: {
            development: {
                options: {
                    paths: ['assets/less']
                },
                files: {
                    'assets/css/fragmenthub.css': 'assets/less/fragmenthub.less',
                    'assets/css/style.css': 'assets/less/style.less',
                    'assets/css/index.css': 'assets/less/index.less',
                    'assets/css/edit.css': 'assets/less/edit.less',
                    'assets/css/post.css': 'assets/less/post.less',
                    'assets/css/login.css': 'assets/less/login.less',
                    'assets/css/signup.css': 'assets/less/signup.less',
                    'assets/css/main.css': 'assets/less/main.less',
                    'assets/css/invite.css': 'assets/less/invite.less',
                    'assets/css/setting.css': 'assets/less/setting.less'
                }
            }
        },
        watch: {
            less: {
                files: ['assets/less/*.less'],
                tasks: ['less']
            },
            /*js: {
                files: ['assets/js/*.js'],
                tasks: ['webpack']
            }*/
        }

    });

    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.loadNpmTasks('grunt-contrib-less');
};
