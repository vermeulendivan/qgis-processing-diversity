import math
from qgis.core import QgsFeatureRequest

def dc_summarizePoly(poly, lyrPoint, fldSpecies):
    dctPoly = {}
    
    # Loop through all of the points is within the polygon's bounding box
    for obs in lyrPoint.getFeatures(QgsFeatureRequest(poly.geometry().boundingBox())):
        # Check to see if the point is within the polygon
        if poly.geometry().contains(obs.geometry()):
            sSpecies = obs.attribute(fldSpecies)  # Species name
            
            # Checks if the species is aleady in the dict
            if sSpecies in dctPoly.keys():
                dctPoly[sSpecies] += 1
            else:
                dctPoly[sSpecies] = 1
    return dctPoly
    

def dc_mergeDictionaries(dMain, cat, dPoly):
    # check if the category exists
    if cat in dMain.keys():
        # if it does then loop through the summary data
        for species, obs in dPoly.items():
            if species in dMain[cat].keys():
                dMain[cat][species] += obs
            else:
                dMain[cat][species] = obs
    else:
        dMain[cat] = dPoly
    return dMain


def dc_richness(dict):
    return len(dict)


def dc_shannons(dict):
    total = sum(dict.values())
    
    shannons = 0
    
    for count in dict.values():
        prop = count/total
        
        shannons += prop * math.log(prop)
    
    return abs(shannons)


def dc_simpsons(dict):
    total = sum(dict.values())
    
    simpsons = 0
    
    for count in dict.values():
        prop = count/total
        
        simpsons += prop * prop
    return simpsons


def dc_evenness(dict):
    max = math.log(dc_richness(dict))
    return dc_shannons(dict) / max


def dc_resultString(dict):
    results = ""
    for category, summary in dict.items():
        results += "{}: {} {:2.3f} {:2.3f} {:2.3f}\n".format(category, dc_richness(summary), dc_shannons(summary), dc_simpsons(summary), dc_evenness(summary))
    return results

def dc_resultHTML(dict, sLayer, sCategory):
    html = """
    <!DOCTYPE html>
    <html>
        <head>
            <title>Diversity calculator</title>
            <style>
                table, th, td {
                    border: 1px solid black;
                }
            </style>
        </head>
        <body>
            <h1>Diversity Calculator output</h1>
            <h2>""" + sLayer + ": " + sCategory + """</h2>
            <table>
                <tr>
                    <th> Name </th><th> Count </th><th> Richness </th><th> Eveness </th><th> Shannons H' </th><th> Simpsons D </th>
                </tr>
        """
    for category in sorted(dict.keys()):
        summary = dict[category]
        html += "           <tr>\n"
        html += "               <td>" + category + "</td>"
        html += "<td>" + str(sum(summary.values())) + "</td>"
        html += "<td>" + "{:3.3f}".format(dc_evenness(summary)) + "</td>"
        html += "<td>" + "{:3.3f}".format(dc_shannons(summary)) + "</td>"
        html += "<td>" + "{:3.3f}".format(dc_simpsons(summary)) + "</td>"
        html += "           </tr>\n"
    html += """
        </table>
    """
    
    return html

