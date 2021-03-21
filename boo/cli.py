import click
import boo.downloader as downloader


@click.group()
def cli():
    """Download 2012-2018 corporate annual financial statements from Rosstat."""
    pass


@cli.command()
@click.argument("year")
def url(year: str):
    """Show URL for remote zipfile."""
    year = accept_year(year)
    click.echo(downloader.RemoteZipFile(year).url, nl=False)


def accept_year(year):
    year = int(year)
    if year in downloader.available_years():
        return year
    else:
        msg = f"{year} is not a valid YEAR, must be in 2012-2018 range."
        click.echo(msg, err=True)
        return None


def on_existing_file(year: int, remote_zip, local_zip):
    click.echo(f"{year} file already exists: {local_zip}")
    if remote_zip.is_same_size(local_zip):
        click.echo("Remote file size equals local file size")
    else:
        click.echo("Found local file of wrong size, delete recommended")


def to_terminal(*args):
    xs = " ".join([str(x) for x in args])
    return click.echo(xs)


@cli.command()
@click.argument("year")
def download(year):
    """Download zip file to local computer."""
    year = accept_year(year)
    if year:
        downloader.download(year, folder=None, echo=to_terminal)


@cli.command()
@click.argument("year")
def unpack(year):
    """Unpack local zip file to get csv file."""
    year = accept_year(year)
    if year:
        downloader.unpack(year, folder=None, echo=to_terminal)


@cli.command()
def years():
    """List available years."""
    click.echo(" ".join([str(x) for x in downloader.available_years()]))


@cli.command()
@click.argument("year", nargs=-1)
def files(year):
    """Show default paths to local zip and csv file by year."""
    click.echo(downloader.default_data_folder())
    if year:
        year = accept_year(year[0])  # check again nargs=-1 makes input a tuple
        if year:
            click.echo(downloader.path_zip(year))
            click.echo(downloader.path_csv(year))


if __name__ == "__main__":
    cli()
