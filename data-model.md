
# DOM HTML
<html>
  <head>
  <body>
    .
    .
    .
    <div id="C_2015103EN.01000601">
      . 
      . zB table, p
      .
      .
      <p id="d1e590-6-1-table" class="ti-tbl">		=> header for table
      <table class="table">				=> table
	<colgroup>
	<tbody>
	  <tr class="table">				=> row
	    <td class="table">
	      <p class="tbl-txt">				=> cell
	    <td class="table">
	  .
	  .
	  .
	  <tr class="table">
	    <td class="table">
	      <p class="tbl-txt">
	    <td class="table">
      <p>
      .
      .
      .
      <p id="d1e1391-6-1-table" class="ti-tbl">
      <table class="table">
      <table class="table">				=> table
	<colgroup>
	<tbody>
	  <tr class="table">				=> row
	    <td class="table">
	      <p class="tbl-txt">				=> cell
	    <td class="table">
	  .
	  .
	  .
	  <tr class="table">
	    <td class="table">
	      <p class="tbl-txt">
	    <td class="table">
      <p>

- datenstruktur geht auch nach letztem land (Zimbabwe) weiter

# structs
**export/import per nation**
"year": int
<country-destination>: {
	"Total": {
		"num-licenses": int
		"val-licenses": int
		"val-arms": int
		"total-eu-licenses-refusals": int
		"criteria-numbers": int
	}
	"CML1": {
		"num-licenses": int
		"val-licenses": int
		"val-arms": int
		"total-eu-licenses-refusals": int
		"criteria-numbers": int
	}
	.
	.
	.
	"CML22": {
		"num-licenses": int
		"val-licenses": int
		"val-arms": int
		"total-eu-licenses-refusals": int
		"criteria-numbers": int
	}
	<country-origin>: {
		"Total": {
			"num-licenses": int
			"val-licenses": int
			"val-arms": int
			"total-eu-licenses-refusals": int
			"criteria-numbers": int
		}
		"CML1": {
			"num-licenses": int
			"val-licenses": int
			"val-arms": int
			"total-eu-licenses-refusals": int
			"criteria-numbers": int
		}
		.
		.
		.
		"CML22": {
			"num-licenses": int
			"val-licenses": int
			"val-arms": int
			"total-eu-licenses-refusals": int
			"criteria-numbers": int
		}
	}
}

**export/import aggregated**
<country-destination>: {
	"CML1": {
		"num-licenses": int
		"val-licenses": int
		"val-arms": int
		"total-eu-licenses-refusals": int
	}
	.
	.
	.
	"CML22": {
		"num-licenses": int
		"val-licenses": int
		"val-arms": int
		"total-eu-licenses-refusals": int
	}
}

# JSON Network

## Edges

## Nodes









