var gulp = require('gulp');
var jshint = require('gulp-jshint');
var gutil = require('gulp-util');

// Check the code quality
gulp.task('qualitychecker', function(cb) {
    return gulp.src([
      'seucorretor/ibuscador/static/**/*.js',
      'seucorretor/themes/static/**/*.js',
      '!seucorretor/themes/static/themes/sydney/js/jquery*.js'])
    .pipe(jshint({esversion: 6}))
    .pipe(jshint.reporter('default'))
    .on('error', gutil.log);
});

gulp.task('default', ['qualitychecker']);
