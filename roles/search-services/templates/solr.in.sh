SOLR_JAVA_MEM="-Xms1g -Xmx1g"
SOLR_OPTS="$SOLR_OPTS -Dsolr.jetty.request.header.size=1000000 -Dsolr.jetty.threads.stop.timeout=300000 -Ddisable.configEdit=true"
SOLR_LOGS_DIR=../../logs
LOG4J_PROPS=$SOLR_LOGS_DIR/log4j.properties
SOLR_OPTS="$SOLR_OPTS -Dsolr.data.dir.root=$DIST_DIR/data -Dsolr.solr.model.dir=$DIST_DIR/data/alfrescoModels"
