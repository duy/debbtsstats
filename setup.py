from setuptools import setup,  find_packages                                    
setup(                                                                          
    name='debbtsstats',                                                           
    version='0.1',                                                              
    description='scripts to generate stadistics from Debian bts.',        
    author='duy',                                                               
    author_email='duy at rhizoma dot tk',                                       
    url='https://github.com/duy/debbtsstats',                                     
    install_requires=[                                                          
        'python-debianbts==1.11',
    ],                                                                          
    setup_requires=[],                                                          
    entry_points = {                                                            
        'console_scripts' : ['bugsbydate = bin.bugsbydate:main',  
            'bugsbypersonbydate = bin.bugsbypersonbydate:main',
            'fetchbtshistory = bin.fetchbtshistory:main']
    },                                                                          
    packages=find_packages(),                                                                                
    keywords = 'python debianbts bts stats',                                             
    license = 'GPLv3+',                                                         
    classifiers=[                                                               
        'Development Status :: 3 - Alpha',                                      
        'Intended Audience :: End Users/Desktop',                               
        'Intended Audience :: Developers',                                      
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: OS Independent',                                   
        'Programming Language :: Python'                                        
        "Topic :: Software Development :: Libraries :: Python Modules",         
    ],                                                                          
)                                                                               
