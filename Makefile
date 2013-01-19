PELICAN=pelican

BASEDIR=$(CURDIR)
INPUTDIR=$(BASEDIR)/content
OUTPUTDIR=$(BASEDIR)/output
CONFFILE=$(BASEDIR)/settings.py

clean:
	find $(OUTPUTDIR) ! -name CNAME  -mindepth 1 -delete

html: clean
	$(PELICAN) $(INPUTDIR) -o $(OUTPUTDIR) -s $(CONFFILE)

github: html 
	ghp-import $(OUTPUTDIR)

