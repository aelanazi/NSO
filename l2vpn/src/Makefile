all:	fxs pylint

# Include standard NCS examples build definitions and rules
include $(NCS_DIR)/src/ncs/build/include.ncs.mk

SRC = $(wildcard yang/*.yang)
FXS = $(SRC:yang/%.yang=../load-dir/%.fxs)

YANGPATH ?= --yangpath yang
YANGPATH += --yangpath ../../cisco-ios/src/ncsc-out/modules/yang
YANGPATH += --yangpath ../../cisco-iosxr/src/ncsc-out/modules/yang
YANGPATH += --yangpath ../../juniper-junos/src/ncsc-out/modules/yang

PYLINT = pylint
PYLINTFLAGS = --disable=R,C --reports=n
PYDIR = ../python
PYTHONFILES = $(wildcard $(PYDIR)/*.py)

pylint: $(patsubst %.py,%.pylint,$(PYTHONFILES))

%.pylint: $(PYLINT) $(PYLINTFLAGS) $*.py || (test $$? -ge 4)

fxs:	$(FXS)

../load-dir/%.fxs:	yang/%.yang
	$(NCSC)  `ls $*-ann.yang  > /dev/null 2>&1 && echo "-a $*-ann.yang"` \
             $(YANGPATH) -c -o $@ $<

clean:
	rm -rf  ../load-dir/*.fxs
