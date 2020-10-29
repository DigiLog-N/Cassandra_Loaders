USE digilog_n;

CREATE TABLE rul_result_live(
	unit int,
	cycle int,
	rul_estimate float,
	primary key ((unit), cycle)
);
