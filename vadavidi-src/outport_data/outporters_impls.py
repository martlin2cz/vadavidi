"""
The outporters impls module.
"""

from typing import Mapping

from outport_data.base_displayers import BaseDisplayer, BaseSeriesStyle
from outport_data.base_outporters import BaseOutporter
from outport_data.base_queriers import BaseQuerier
from outport_data.base_query import Query
from outport_data.base_raisers import BaseRaiser


################################################################################
class DefaultOutporter(BaseOutporter):
    
    # the raiser
    raiser: BaseRaiser
    
    # the querier
    querier: BaseQuerier
    
    # the displayer
    displayer: BaseDisplayer
 
    # the supported queries
    queries: Mapping[str, Query]
    
    # the supported display configurations
    configs: Mapping[str, Mapping[str, BaseSeriesStyle]]
    
    def run(self, dataset_name, schema, query_name, x_axis_name):
        
        table = self.raiser.run(dataset_name, schema)
        
        query = self.queries[query_name]
        table = self.querier.query(dataset_name, table, query)
        
        styles = self.configs[query_name]
        series_names = list(styles.keys())
        self.displayer.show(dataset_name, table, x_axis_name, series_names, styles)
        
        

################################################################################        