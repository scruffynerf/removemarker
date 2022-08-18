import json
import sys
import os

# if you put this into a subdirectory of scrapers, and pycommon is in scraper
sys.path.insert(0,'..')

try:
    import py_common.graphql as graphql
    import py_common.log as log
except ModuleNotFoundError:
    print("You need to download the folder 'py_common' from the community repo! (CommunityScrapers/tree/master/scrapers/py_common)", file=sys.stderr)
    sys.exit()

'''  This script runs a graphql function to remove all markers from a scene
     '''

def call_graphql(query, variables=None):
    return graphql.callGraphQL(query, variables)

def get_id(obj):
    ids = []
    for item in obj:
        ids.append(item['id'])
    return ids

def remove_markers(sceneid):
    query = """
            query findSceneMarkers($id: ID!){
                      findScene(id: $id) {
  	                  scene_markers{
    	                      id
  	                  }
	              }
                  }
            """
    variables = {
        "id": sceneid
    }
    result = call_graphql(query, variables)
    if result:
        markers = get_id(result["findScene"]["scene_markers"])
        log.debug(markers)
        log.info("Deleting Scene Markers")
        query = "mutation markerdelete($id: ID!){ sceneMarkerDestroy(id: $id) }"
        for marker in markers:
          variables = {"id": marker}
          result = call_graphql(query, variables)
          if result["sceneMarkerDestroy"]:
             log.debug(f"Deleted Marker {marker}")
          else:
             log.debug(f"Error deleting Marker {marker}")
             log.debug(result)
    return

FRAGMENT = json.loads(sys.stdin.read())
SCENE_ID = FRAGMENT.get("id")
scene = graphql.getScene(SCENE_ID)
if scene:
    remove_markers(SCENE_ID)
print(json.dumps({}))

# Last Updated August 14, 2022

