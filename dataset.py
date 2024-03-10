import numpy as np
from pathlib import Path
import yaml

class run_dataset:
    
    def __init__(self,run_id=[], date=[], initialize_separate_lists=False):   
        """
        Initialize the class run_dataset
        
        Parameters
        ----------
        run_id : list
        date : list
        initialize_separate_lists : bool
                
        If initialize_separate_lists is True: 
            - run_id is a list of list with the run ids of the same date in a single list.
            - date is a single list with the dates. Dimension 1 correspond to the date for the
              list in the dimension 1 of run_id.
        If initialize_separate_lists is False:
            - run_id is a single list with all the run ids.
            - date is a single list with the date of the run id in the same dimension.
            
        Example
        -------
        Use initialize_separate_lists as True
        >>> #dates of the runs
        >>> days=[20201120, 20210904, 20210905]
        >>> #list with the IDs of the runs for each day
        >>> runs1=[2965,2966]
        >>> runs2=[6044]
        >>> runs3=[6071,6072]
        >>> #group all list of ID runs in the same list
        >>> day_runs=[runs1, runs2,runs3]
        >>> #create the dataset
        >>> run_dataset(day_runs,days,True)
        
        Use initialize_separate_lists as False. Using the previous example        
        >>> #Produce two list where the index gives the date and run ID
        >>> array_runs=[]
        >>> for i,dayrun in enumerate(day_runs):
        >>>     for run in dayrun:
        >>>         array_runs.append([days[i],run])    
        >>> array_runs=np.array(array_runs)
        >>> #fill the run_dataset class
        >>> dataset=run_dataset(array_runs[:,1],array_runs[:,0])
        """
                    
        runs=[]
        if initialize_separate_lists:
            array_runs=[]
            for i,dayrun in enumerate(run_id):
                for run in dayrun:
                    array_runs.append([date[i],run])

            array_runs=np.array(array_runs)
            run_id=array_runs[:,1]
            date=array_runs[:,0]            

        self.id=run_id
        self.date=date
        runs.append(self)
        
    def sort_runs_by_date(self,day):
        """
        Find the runs taken for a specific date.
        
        Parameters
        ----------
        day: int
            Date of interest. Format: YYYYMMDD.

        Returns
        -------
        list_run_id: np.array
            List of run ids that were taken the date "day".
        """
        
        import numpy as np
        list_run_id=[]
        #loop for each run if there is more than one
        if len(np.shape(self.id))>=1:
            for irun in range(len(self.id)):
                if day==self.date[irun]:
                    list_run_id.append(self.id[irun])
        #if only one run it is returned
        else:
            list_run_id.append(self.id)     
        return np.array(list_run_id)
    
    def sort_date_by_run(self,run_id):
        """
        Find the date of a specific run id.
        
        Parameters
        ----------
        run_id: int
            Run id of interest.
            
        Returns
        -------
        date: int
            Date for which run_id was taken.
        """
        
        import numpy as np
        if len(np.shape(self.date))>=1:
            for idate in range(len(self.date)):
                if run_id==self.id[idate]:
                    return self.date[idate]
        else:
            return self.date

    def number_of_days(self):
        """
        Obtain the total number of days.
        
        Returns
        -------
        days: np.array
            List of days.
        """
        
        import numpy as np
        days=[]
        if len(np.shape(self.id))>=1:
            for irun in range(len(self.id)):
                days.append(self.date[irun])
        else:
            days.append(self.date)
        return np.unique(days)
    
    def number_of_runs(self):
        """
        Obtain the total number of run ids.
        
        Returns
        -------
        runs: np.array
            List of run ids.
        """
        
        import numpy as np
        runs=[]
        if len(np.shape(self.id))>=1:
            for irun in range(len(self.id)):
                runs.append(self.id[irun])
        else:
            runs.append(self.id)
        return np.unique(runs)    
    
    
    def read_dataset(self, file_name):
        """
        Read a dataset from a yaml file.
        
        Parameters        
        ----------
        file_name: str
        Path and file name of the yaml file with the dataset
        
        """
        import yaml

        if not Path(file_name).exists():
            raise FileNotFoundError(f"File {file_name} does not exist")

        with open(file_name, 'r') as file:
            data = yaml.safe_load(file)

        dates = list(data.keys())
        run_list = []
        for key in dates:
            run_list.append(data[key])

        # Initialize the run_dataset object with the data read from the file
        self.__init__(run_list, dates, True)
        
        
    def write_dataset(self, file_name):
        """
        Write to yaml file the dataset. The keys are the dates
        and the values in the keys are the run_ids for that
        date.
        
        Parameters        
        ----------
        file_name: str
        Path and file name of the yaml file with the dataset
        
        """
        
        dataset_dict={}
        for date in self.number_of_days():
            dataset_dict[int(date)]=self.sort_runs_by_date(date).tolist()

        with open(file_name, 'w') as file:
            yaml.dump(dataset_dict, file, indent=4, default_flow_style=True)