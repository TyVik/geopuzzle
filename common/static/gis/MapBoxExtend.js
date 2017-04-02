MapWidget.prototype.downloadFeatures = function(feat) {
    console.log(this.read_wkt(document.getElementById(this.options.id).value));
};

MapWidget.prototype.uploadFeatures = function(feat) {
	return "SRID=" + this.options.map_srid + ";" + this.wkt_f.write(feat);
};

