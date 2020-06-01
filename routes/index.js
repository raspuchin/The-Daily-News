var express = require('express');
var router = express.Router();

/* GET about page. */
router.get('/about', function (req, res, next) {
    res.render('about', { title: 'The Daily News' });
});

/* GET contact page. */
router.get('/contact', function (req, res, next) {
    res.render('contact', { title: 'The Daily News' });
});

/* API Home*/
router.get('/api/home', function (req, res) {
    var db = req.db;
    var collection = db.get('articlesData');
    collection.find({ sentiment: '[1]' }, { limit: 100 }, function (e, docs) {
        res.json({
            home: docs,
        });
    });
});

/* GET home page. */
router.get('/', function (req, res) {
    var db = req.db;
    var collection = db.get('articlesData');
    collection.find({}, {}, function (e, docs) {
        res.render('home', {
            home: docs,
        });
    });
});

/* GET home page. */
router.get('/home', function (req, res) {
    var db = req.db;
    var collection = db.get('articlesData');
    collection.find({}, {}, function (e, docs) {
        res.render('home', {
            home: docs,
        });
    });
});

/* GET india page. */
router.get('/india', function (req, res) {
    var db = req.db;
    var collection = db.get('articlesData');
    collection.find({}, {}, function (e, docs) {
        res.render('india', {
            home: docs,
        });
    });
});

/* GET entertainment page. */
router.get('/entertainment', function (req, res) {
    var db = req.db;
    var collection = db.get('articlesData');
    collection.find({}, {}, function (e, docs) {
        res.render('entertainment', {
            home: docs,
        });
    });
});

/* GET tech page. */
router.get('/technology', function (req, res) {
    var db = req.db;
    var collection = db.get('articlesData');
    collection.find({}, {}, function (e, docs) {
        res.render('technology', {
            home: docs,
        });
    });
});

/* GET business page. */
router.get('/business', function (req, res) {
    var db = req.db;
    var collection = db.get('articlesData');
    collection.find({}, {}, function (e, docs) {
        res.render('business', {
            home: docs,
        });
    });
});

/* GET sports page. */
router.get('/sports', function (req, res) {
    var db = req.db;
    var collection = db.get('articlesData');
    collection.find({}, {}, function (e, docs) {
        res.render('sports', {
            home: docs,
        });
    });
});

/* GET world page. */
router.get('/world', function (req, res) {
    var db = req.db;
    var collection = db.get('articlesData');
    collection.find({}, {}, function (e, docs) {
        res.render('world', {
            home: docs,
        });
    });
});

module.exports = router;
