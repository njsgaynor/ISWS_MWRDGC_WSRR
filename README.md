# ISWS_MWRDGC_WSRR
Code repository for automation scripts related to the Metropolitan Water
Reclamation District of Greater Chicago Watershed Release Rate project
at the Illinois State Water Survey (2015-2016)

InitHMS.py is the main script in this package. It can be run directly or
imported as a module and run using InitHMS.main(config). This was
developed using Python 2.7.5.

How to run:
1. Modify HMSconfig.py to find the files that need to be modified.
2. Type "python InitHMS > InitHMS.out" into the Windows command line.

Structure:
InitHMS.py
    -description: drives the process of splitting subbasins in the
    specified (sub)watershed
    -depends on: contents of hecElements, Subwatershed_class, 
    Tablenames_class, SBDict_class
    -UpdatePdataFile(pd, pdatasink): not currently used.
    -readBasinFile(ws): reads the input *.basin file, splits subbasins
    (and does related tasks via imported modules, and writes updated
    *.basin file
    -modMetFile(metFile, metData, hmsPath, sbList): adds the new
    subbasins to the relevant *.met file
    -main(config): drives the workflow

Subwatershed_class.py
    -description: 
    -depends on: 
    -


SBDict_class.py
    -description: dictionary class that contains
    subbasin_name:release rate pairs
    -depends on: None
    -__init__: instantiates basic dictionary
    -add(x): adds x to the dictionary, where x is a {"key":value} pair
    -remove(x): deletes item with key x from the dictionary
    -getKeys: returns the keys in the dictionary
    -getValues: returns the values in the dictionary
    -writeSbPairs(sbOut): writes entire dictionary to JSON file
    specified in sbOut

TableNames_class.py
    -description: list class that contains a list of lists,
    where the sublist includes subbasin name, table name,
    subbasin area, and release rate
    -depends on: None
    -__init__: instantiates basic list
    -append(x): adds x to the end of the list
    -remove(x): finds x and removes it from the list
    -writeTableFile(tableOut): writes table to JSON file tableOut
    
Contents of hecElements:
Property_class.py
    -description: dictionary class that contains 
    property_name:property_value pairs, which are the basis for named
    properties in the Elements class (and its child classes)
    -depends on: None
    -__init__(name): instantiates dictionary with key set to name and
    value set to None
    -newProperty(name, value) [classmethod]: instantiates new Property
    with key of name and value of value
    -getValue: returns value of Property instance
    -getAsFloat: returns value as float; error if cannot be converted
    -getAsString: returns value as string; error if cannot be converted
    -getName: returns key of Property instance
    -setName(name): sets key to name

Element_class.py
    -description: list class that contains Property instances; parent
    class for types of elements in *.basin HEC-HMS files
    -depends on: Property_class
    -__init__(category, identifier): instantiates Element with category
    and identifier set to input values
    -getIdentifer: returns value of identifer
    -setIdentifer(identifier): sets identifier property to input
    -getCategory: returns value of category
    -setCategory(category): sets category property to input
    -deserialize(currentLine, infile): reads a single element from *.basin
    input file starting at line currentLine
    -serialize(outfile): writes a single element to *.basin output file
    -add(x): adds Property x to an Element instance
    -remove(x): removes Property x from an Element instance; returns error
    if property does not exit in Element instance

Basin_class.py
    -description: list class that contains Property instances for Basin
    items in *.basin HEC-HMS files
    -depends on: Element_class
    -__init__: instantiates an Element with category "Basin"
    -readBasin(currentLine, basinsrc, basinsink) [classmethod]: reads a
    single Basin element from *.basin input file and writes it to 
    *.basin output file; returns Basin instance.

Subbasin_class.py
    -description: list class that contains Property instances for
    Subbasin items in *.basin HEC-HMS files
    -depends on: Element_class, Property_class, Junction_class, 
    Reservoir_class, copy
    -__init__: instantiates an Element with category "Subbasin" and 
    Properties for area, downstream, curve number, percent impervious
    area, canvas x, canvas y, canopy, release rate, and percent
    redevelopment; Property values set to None
    -readSubbasin(currentLine, basinsrc, basinsink) [classmethod]: reads
    a single Subbasin element from *.basin input file. Calls functions
    that divide the subbasin, add a reservoir, and add a junction.
    Assigns values as appropriate to pre-defined Properties.
    Writes Subbasin element to *.basin output file; returns Subbasin
    instance with Properties updated to reflect subbasin division, new 
    subbasin, and name of storage-outflow table for new subbasin.
    -add(x): adds Property x to instance of Subbasin, using pre-defined
    Property if available; error if x is not an instance of Property.
    -remove(x): removes x from instance of Subbasin or assigns value of
    None if it is a pre-defined Property; returns error if not found.
    -divideSubbasin(basinsink, redevel, curvenum, rlsrate): Divides 
    subbasin based on percent redevelopment with new subbasin occupying
    the portion that is redeveloped and old subbasin area reduced to the
    remainder. Calls functions to create new Subbasin, Junction, and 
    Reservoir instances. Routes new subbasin through Reservoir to
    Junction and old subbasin directly to Junction so that measurements
    at Junction are for entire subbasin (new + old). Sets release rate
    and redevelopment percent of new subbasin.
    -newSubbasin(s, basinsink, redevel, curvenum) [classmethod]: copies
    Subbasin s to new instance of Subbasin. Sets properties to reflect
    characteristics of redeveloped area. Writes new subbasin to *.basin
    output file. Returns Subbasin instance of new subbasin.    

Junction_class.py
    -description: list class that contains Property instances for
    Junction items in *.basin HEC-HMS files
    -depends on: Element_class, Property_class
    -__init__: instantiates an Element with category "Junction" and 
    Property for downstream; Property value set to None
    -readJunction(currentLine, basinsrc, basinsink) [classmethod]: reads
    a single Junction element from *.basin input file. Writes Junction
    element to *.basin output file; returns Junction instance.
    -add(x): adds Property x to instance of Junction, using pre-defined
    Property if available; error if x is not an instance of Property.
    -remove(x): removes x from instance of Junction or assigns value of
    None if it is a pre-defined Property; returns error if not found.
    -newJunction(s, basinsink) [classmethod]: instantiates new Junction
    and sets properties as appropriate based on those in Subbasin s.
    Writes Junction element to *.basin output file. Returns instance
    of Junction.

Reservoir_class.py
    -description: list class that contains Property instances for
    Reservoir items in *.basin HEC-HMS files
    -depends on: Element_class, Property_class
    -__init__: instantiates an Element with category "Reservoir" and 
    Properties for downstream and storage-outflow table; Property values
    set to None.
    -readReservoir(currentLine, basinsrc, basinsink, redevel, rlsrate)
    [classmethod]: reads a single Reservoir element from *.basin input
    file. Writes Reservoir element to *.basin output file; returns 
    instance of Reservoir.
    -add(x): adds Property x to instance of Reservoir, using pre-defined
    Property if available; error if x is not an instance of Property.
    -remove(x): removes x from instance of Reservoir or assigns value of
    None if it is a pre-defined Property; returns error if not found.
    -newReservoir(s, basinsink) [classmethod]: instantiates new Reservoir
    and sets properties as appropriate based on those in Subbasin s. Sets
    storage-outflow table name based on subbasin name, % redevelopment,
    and release rate. Writes Reservoir element to *.basin output file.
    Returns instance of Reservoir.

Reach_class.py
    -description: list class that contains Property instances for
    Reach items in *.basin HEC-HMS files
    -depends on: Element_class, Property_class
    -__init__: instantiates an Element with category "Reach" and 
    Property for downstream; Property value set to None.
    -readReach(currentLine, basinsrc, basinsink) [classmethod]: reads a 
    single Reach element from *.basin input file. Writes Reach
    element to *.basin output file; returns instance of Reach.
    -add(x): adds Property x to instance of Reach, using pre-defined
    Property if available; error if x is not an instance of Property.
    -remove(x): removes x from instance of Reach or assigns value of
    None if it is a pre-defined Property; returns error if not found.

Diversion_class.py
    -description: list class that contains Property instances for
    Diversion items in *.basin HEC-HMS files
    -depends on: Element_class, Property_class
    -__init__: instantiates an Element with category "Diversion" and 
    Properties for downstream and divert to; Property values set to None.
    -readDiversion(currentLine, basinsrc, basinsink) [classmethod]: reads a 
    single Diversion element from *.basin input file. Writes Diversion
    element to *.basin output file; returns instance of Diversion.
    -add(x): adds Property x to instance of Diversion, using pre-defined
    Property if available; error if x is not an instance of Property.
    -remove(x): removes x from instance of Diversion or assigns value of
    None if it is a pre-defined Property; returns error if not found.

Sink_class.py
    -description: list class that contains Property instances for Sink
    items in *.basin HEC-HMS files
    -depends on: Element_class
    -__init__: instantiates an Element with category "Sink"
    -readSink(currentLine, basinsrc, basinsink) [classmethod]: reads a
    single Sink element from *.basin input file and writes it to 
    *.basin output file; returns instance of Sink.

BasinSchema_class.py
    -description: list class that contains Property instances for Basin
    Schematic Properties items in *.basin HEC-HMS files
    -depends on: Element_class
    -__init__: instantiates an Element with category "Basin Schematic
    Properties"
    -readBasinSchema(currentLine, basinsrc, basinsink) [classmethod]:
    reads a single Basin Schematic Properties element from *.basin input
    file and writes it to *.basin output file; returns instance of
    BasinSchema.

Pdata_class.py
    -description: 
    -depends on: Element_class, Property_class, datetime.datetime,
    calendar
    -__init__: instantiates new Element item with category "Table" and
    Properties for DSS file where 