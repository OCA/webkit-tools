Report Archive
This module extends the functionality of webkit_report and allows you to archive the reports to be printed into the file system of the same machine that is running the OpenERP instance.

Configuration
	·A system parameter must be set up in order to make the storage possible. This parameter must have as key: "archive_reports_path" and as value the absolute path to the directory where the reports will be saved.
	·Go to Actions -> Reports. Two new fields will be displayed: "Archive the file" and "Save as File Prefix". Select those reports that you want to be stored by clicking the "Archive the File" flag and set a name for each by typing into the "Save as File Prefix" field. You can use python expression e.g. object.name. The directory must exist.
	·If the directory is not specified or a name for the report has not been provided the file will not be saved into the file system.

Usage
Just print the report as usual. Apart from the report returned to the browser a copy of it will be saved in the specified directory.
