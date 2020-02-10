import os
from zipfile import ZipFile

class IndicatorExportService:
    def __init__(self, site_directory, indicators):
        """Constructor for IndicatorExportService.

        Parameters
        ----------
        site_directory : string
            Path to an already-performed build. The files to be zipped are
            assumed to be in a "data" subfolder.
        indicators : dict
            A dict of Indicator objects, keyed by indicator id.
        """
        self.__site_directory = site_directory
        self.__zip_directory = "%s/zip" % site_directory
        self.__data_directory = "%s/data" % site_directory
        self.__indicators = indicators

    def export_all_indicator_data_as_zip_archive(self):
        self.__create_zip_folder_at_site_directory()
        csv_files = self.__get_all_indicator_csv_files()
        self.__create_zip_file("all_indicators.zip", csv_files)

    def __create_zip_folder_at_site_directory(self):
        directory = "%s/zip" % self.__site_directory
        if not os.path.exists(directory):
            os.mkdir(directory)

    def __get_all_indicator_csv_files(self):
        all_data_file_names = os.listdir(self.__data_directory)
        csv_data_file_names = []
        for file_name in all_data_file_names:
            if self.__file_is_csv(file_name) and self.__file_is_suitable_for_export(file_name):
                csv_data_file_names.append(file_name)

        csv_data_files = []
        for each_file_name in csv_data_file_names:
            csv_data_files.append({
                "file_name": each_file_name,
                "path": "%s/%s" % (self.__data_directory, each_file_name)
            })

        return csv_data_files

    def __file_is_csv(self, file_name):
        return file_name.endswith(".csv")

    def __file_is_suitable_for_export(self, file_name):
        indicator_id = file_name.split('.')[0]
        if indicator_id not in self.__indicators:
            raise KeyError("Could not check whether %s is complete." % indicator_id)
        suitable = True
        suitable = suitable & self.__indicators[indicator_id].is_complete()
        suitable = suitable & self.__indicators[indicator_id].is_statistical()
        return suitable

    def __create_zip_file(self, zip_file_name, files_to_include):
        zip_file = ZipFile("%s/%s" % (self.__zip_directory, zip_file_name), "w")

        for each_file in files_to_include:
            zip_file.write(each_file["path"], each_file["file_name"])

        zip_file.close()