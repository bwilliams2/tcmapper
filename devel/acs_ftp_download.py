#%%
from ftplib import FTP
census = FTP("ftp2.census.gov")
census.login()

#%%
#route to programs_surveys
[census.cwd(folder) for folder in ["programs-surveys", "acs", "summary_file"]]
# %%
census.retrlines("LIST")
# %%
census.nlst()

# %%
years = census.nlst()
for year in years[1:]:
    census.cwd(year)
    census.cwd("data")
    census.cwd("1_year")
    census.cwd("Minnesota")
    #%%
    from pathlib import Path
    census.nlst()
    all_zip = [file for file in census.nlst() if "all" in file][0]
    data_folder = Path(f"../data/census/{year}")
    data_folder.mkdir(parents=True, exist_ok=True)
    with data_folder.joinpath(all_zip).open("wb") as f:
        census.retrbinary(f'RETR {all_zip}', f.write)
    census.cwd("..")
    census.cwd("..")
    census.cwd("documentation")
    wb = [file for file in census.nlst() if "xls" in file][0]
    with data_folder.joinpath(wb).open("wb") as f:
        census.retrbinary(f'RETR {wb}', f.write)
    census.cwd("..")
    census.cwd("..")
# %%
census.retrlines("LIST")
# %%

census.nlst()
# %%
census.cwd("..")
# %%
census.nlst()
# %%
