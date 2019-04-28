What about running nose with a smarter interactive debugger?

Use this and *never* risk yourself forgetting `import ipdb; ipdb.set_trace()` in your code again!

This plugin serves to launch ipdb or ipydex.IPS (i.e. embedded IPython shell) after an test failure or error. 

This plugin is about 95% based on nose's builtin [builtin debug plugin][1].


Change Note
-----------
The present version is a fork of <http://github.com/flavioamieiro/nose-ipdb>.
It has several improvements:

- Possibility to launch IPython shell instead of debugger
- Pretty formated Traceback
- Better comaptibility with unittest-package (select meaningful frame to launch ipdb/ips inside)

Feal free to open an issue or send feedback to `"Carsten.+".replace('+', 'Knoll@') + "tu-dresden.de"`  

Install
--------

    pip install ipdbplugin

Usage
------

To drop into ipdb on errors:

    nosetests --ipdb

To drop into ipdb on failures:

    nosetests --ipdb-failures

**New in this fork:** Drop into IPython embedded shell on failures or errors:

    nosetests --ips

License
--------

GNU Lesser General Public License

Authors
--------

* Bernardo Fontes (falecomigo@bernardofontes.net)
* Flávio Amieiro (amieiro.flavio@gmail.com)
* Henrique Bastos (henrique@bastos.net)


[1]: http://www.somethingaboutorange.com/mrl/projects/nose/0.11.2/plugins/debug.html
