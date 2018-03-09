<%!
    import os

    import autosubliminal
    from autosubliminal.utils import convert_timestamp, display_item, display_title, get_file_size, count_wanted_items
    from autosubliminal.wanteditem import WantedItem
%>

<%block name="bodyContent">

    <%
        total = count_wanted_items()
        total_shows = count_wanted_items('episode')
        total_movies = count_wanted_items('movie')
    %>

    <div class="container">

        <div class="panel panel-default">

            <div class="panel-heading">
                <span class="h3 weighted">Wanted (${total}) - Shows (${total_shows}) - Movies (${total_movies})</span>
            </div>

            <div class="panel-body">

                <div class="form-inline">
                    <div class="row">
                        <div class="col-xs-12 col-sm-6 col-md-6 table-filter left">
                            <div class="input-group">
                                <span class="input-group-addon table-filter-label">Video type</span>
                                <select id="wanteditemstypefilter" class="wanteditemsfilter form-control input-sm" type="search" data-column="0">
                                    <option value="">All</option>
                                    <option value="episode">Shows</option>
                                    <option value="movie">Movies</option>
                                </select>
                            </div>
                        </div>
                        <div class="col-xs-12 col-sm-6 col-md-6 table-filter right">
                            <div class="input-group">
                                <span class="input-group-addon table-filter-label">Search</span>
                                <input id="wanteditemssearchfilter" class="wanteditemsfilter form-control input-sm" type="search" data-column="all">
                                <span class="input-group-addon wanteditemsfilterreset">
                                    <i class="fa fa-times" aria-hidden="true"></i></span>
                            </div>
                        </div>
                    </div>
                </div>

                <table id="wanteditems" class="table table-condensed table-striped table-hover">

                    <thead>
                    <tr>
                        <th class="hidden">Type</th>
                        <th>Show/Movie name</th>
                        <th>Season</th>
                        <th>Episode</th>
                        <th>Source</th>
                        <th>Quality</th>
                        <th>Codec</th>
                        <th>Group</th>
                        <th>Lang</th>
                        <th>Time</th>
                    </tr>
                    </thead>

                    <tbody>
                        % for index, item in enumerate(autosubliminal.WANTEDQUEUE):
                            <% rowClass = 'wanted-item' if WantedItem(item).search_active else 'wanted-item inactive' %>
                            <tr class="${rowClass}">
                                <td class="hidden">${item['type']}</td>
                                <td>
                                    <span class="dropdown">
                                        <a class="dropdown-toggle wanted-item-title main-column" data-toggle="dropdown" title="Click to skip">${display_title(item)}</a>
                                        % if item['type'] == 'episode':
                                            <ul class="dropdown-menu has-tip">
                                                <li>
                                                    <a href="${autosubliminal.WEBROOT}/home/postProcess/${index}">Skip and post process show</a>
                                                </li>
                                                <li>
                                                    <a href="${autosubliminal.WEBROOT}/home/deleteVideo/${index}">Skip and delete show</a>
                                                </li>
                                                <li>
                                                    <a href="${autosubliminal.WEBROOT}/home/skipShow/${index}/${item['title']}">Skip show</a>
                                                </li>
                                                <li>
                                                    <a href="${autosubliminal.WEBROOT}/home/skipShow/${index}/${item['title']}/${item['season']}">Skip season ${item['season']}</a>
                                                </li>
                                            </ul>
                                        % elif item['type'] == 'movie':
                                            <ul class="dropdown-menu has-tip">
                                                <li>
                                                    <a href="${autosubliminal.WEBROOT}/home/postProcess/${index}">Skip and post process movie</a>
                                                </li>
                                                <li>
                                                    <a href="${autosubliminal.WEBROOT}/home/deleteVideo/${index}">Skip and delete movie</a>
                                                </li>
                                                <li>
                                                    <a href="${autosubliminal.WEBROOT}/home/skipMovie/${index}/${item['title']}/${item['year']}">Skip movie</a>
                                                </li>
                                            </ul>
                                        % endif
                                    </span>
                                    <span class="dropdown">
                                        <a class="dropdown-toggle" data-toggle="dropdown">
                                            <i class="fa fa-info-circle" aria-hidden="true" title="Click for more info"></i>
                                        </a>
                                        <ul class="dropdown-menu has-tip info-list">
                                            <li>
                                                <span class="info-list-label">File name:</span>
                                                <span>${os.path.basename(item['videopath'])}</span>
                                            </li>
                                            <li>
                                                <span class="info-list-label">File size:</span>
                                                <span>${get_file_size(item['videopath'])}</span>
                                            </li>
                                        </ul>
                                    </span>
                                    % if item['type'] == 'episode':
                                        % if not item['tvdbid']:
                                            <span class="dropdown">
                                                <a class="dropdown-toggle" data-toggle="dropdown">
                                                    <i class="fa fa-exclamation-triangle text-danger" aria-hidden="true" title="Tvdb id could not be found!"></i>
                                                </a>
                                                <ul class="dropdown-menu has-tip info-list">
                                                    <li>
                                                        <a href="${autosubliminal.WEBROOT}/home/searchId/${index}">Search tvdb id</a>
                                                    </li>
                                                </ul>
                                            </span>
                                        % else:
                                            <span>
                                                <a href="${autosubliminal.DEREFERURL}${autosubliminal.TVDBURL}${item['tvdbid']}" target="_blank">
                                                    <i class="fa fa-television" aria-hidden="true" title="Click to visit Tvdb"></i>
                                                </a>
                                            </span>
                                        % endif
                                    % elif item['type'] == 'movie':
                                        % if not item['imdbid']:
                                            <span class="dropdown">
                                                <a class="dropdown-toggle" data-toggle="dropdown">
                                                    <i class="fa fa-exclamation-triangle text-danger" aria-hidden="true" title="Imdb id could not be found!"></i>
                                                </a>
                                                <ul class="dropdown-menu has-tip info-list">
                                                    <li>
                                                        <a href="${autosubliminal.WEBROOT}/home/searchId/${index}">Search imdb id</a>
                                                    </li>
                                                </ul>
                                            </span>
                                        % else:
                                            <span>
                                                <a href="${autosubliminal.DEREFERURL}${autosubliminal.IMDBURL}${item['imdbid']}" target="_blank">
                                                    <i class="fa fa-imdb" aria-hidden="true" title="Click to visit Imdb"></i>
                                                </a>
                                            </span>
                                        % endif
                                    % endif
                                    % if autosubliminal.MANUALREFINEVIDEO:
                                        <span class="dropdown">
                                            <a class="dropdown-toggle" data-toggle="dropdown">
                                                <i class="fa fa-pencil" aria-hidden="true" title="Click to manually update show/movie details"></i>
                                            </a>
                                            <ul class="dropdown-menu has-tip info-list">
                                                <li>
                                                    <div class="panel panel-default">
                                                        <div class="panel-heading text-center">
                                                            <span class="info-list-label">Update show/movie details</span>
                                                        </div>
                                                        <div class="panel-body text-right">
                                                            <div class="form-inline form-group narrow">
                                                                <span class="info-list-label">Title:</span>
                                                                <input type="text" value="${display_item(item, 'title')}" class="form-control input-sm update-wanted-item-title">
                                                            </div>
                                                            <div class="form-inline form-group narrow">
                                                                <span class="info-list-label">Year:</span>
                                                                <input type="text" value="${display_item(item, 'year')}" class="form-control input-sm update-wanted-item-year">
                                                            </div>
                                                            <div class="form-inline form-group narrow">
                                                                <span class="info-list-label">Season:</span>
                                                                <input type="text" value="${display_item(item, 'season')}" class="form-control input-sm update-wanted-item-season">
                                                            </div>
                                                            <div class="form-inline form-group narrow">
                                                                <span class="info-list-label">Episode:</span>
                                                                <input type="text" value="${display_item(item, 'episode')}" class="form-control input-sm update-wanted-item-episode">
                                                            </div>
                                                            <div class="form-inline form-group narrow">
                                                                <span class="info-list-label">Source:</span>
                                                                <input type="text" value="${display_item(item, 'source')}" class="form-control input-sm update-wanted-item-source">
                                                            </div>
                                                            <div class="form-inline form-group narrow">
                                                                <span class="info-list-label">Quality:</span>
                                                                <input type="text" value="${display_item(item, 'quality')}" class="form-control input-sm update-wanted-item-quality">
                                                            </div>
                                                            <div class="form-inline form-group narrow">
                                                                <span class="info-list-label">Codec:</span>
                                                                <input type="text" value="${display_item(item, 'codec')}" class="form-control input-sm update-wanted-item-codec">
                                                            </div>
                                                            <div class="form-inline form-group narrow">
                                                                <span class="info-list-label">Group:</span>
                                                                <input type="text" value="${display_item(item, 'releasegrp')}" class="form-control input-sm update-wanted-item-releasegrp">
                                                            </div>
                                                            <a href="${autosubliminal.WEBROOT}/home/resetWantedItem/${index}" class="btn btn-sm btn-default reset-wanted-item-link">Reset</a>
                                                            <a href="${autosubliminal.WEBROOT}/home/updateWantedItem/${index}" class="btn btn-sm btn-default update-wanted-item-link">Update</a>
                                                        </div>
                                                    </div>
                                                </li>
                                            </ul>
                                        </span>
                                    % endif
                                </td>
                                <td class="wanted-item-season">
                                    ${display_item(item, 'season')}
                                </td>
                                <td class="wanted-item-episode">
                                    ${display_item(item, 'episode')}
                                </td>
                                <td class="wanted-item-source wrapped">
                                    ${display_item(item, 'source', 'N/A', True)}
                                </td>
                                <td class="wanted-item-quality wrapped">
                                    ${display_item(item, 'quality', 'N/A', True)}
                                </td>
                                <td class="wanted-item-codec wrapped">
                                    ${display_item(item, 'codec', 'N/A', True)}
                                </td>
                                <td class="wanted-item-releasegrp wrapped">
                                    ${display_item(item, 'releasegrp', 'N/A', True)}
                                </td>
                                <td class="wanted-item-languages">
                                    % for lang in item['languages']:
                                    <% imageurl = autosubliminal.WEBROOT + "/images/flags/language/" + lang + ".png" %>
                                        <span class="dropdown">
                                            <a class="dropdown-toggle" data-toggle="dropdown">
                                                <img src="${imageurl}" class="language-icon" alt="${lang}" title="Click to search manually">
                                            </a>
                                            <ul class="dropdown-menu pull-right no-padding">
                                                <li>
                                                    <div class="panel panel-default container-manualsearch">
                                                        <div class="panel-heading">
                                                            <a class="container-manualsearch-link" href="${autosubliminal.WEBROOT}/home/searchSubtitle/${index}/${lang}">
                                                                Manual search
                                                            </a>
                                                            <i class="fa fa-spinner fa-spin fa-fw invisible" title="Searching..."></i>
                                                            <span class="sr-only">Searching...</span>
                                                        </div>
                                                        <div class="panel-body"></div>
                                                    </div>
                                                </li>
                                            </ul>
                                        </span>
                                    % endfor
                                </td>
                                <td class="wanted-item-timestamp datetime">
                                    ${convert_timestamp(item['timestamp'])}
                                </td>
                            </tr>
                        % endfor
                    </tbody>

                </table>

                <div id="wanteditemspager" class="pager">
                    <% image_base_url = autosubliminal.WEBROOT + "/images/vendor/tablesorter" %>
                    <img src="${image_base_url}/first.png" class="first"/>
                    <img src="${image_base_url}/prev.png" class="prev"/>
                    <span class="pagedisplay"></span>
                    <!-- this can be any element, including an input -->
                    <img src="${image_base_url}/next.png" class="next"/>
                    <img src="${image_base_url}/last.png" class="last"/>
                    <select class="pagesize" title="Select page size">
                        <option value="10">10</option>
                        <option value="20">20</option>
                        <option value="30">30</option>
                        <option value="40">40</option>
                        <option value="50">50</option>
                        <option value="all">All</option>
                    </select>
                    <select class="gotoPage" title="Select page number"></select>
                </div>

            </div>

            <div class="panel-footer">
                <div class="note">
                    <div>Click 'Show/Movie name' for skip functionality</div>
                    <div>Click 'Language' icon for manual search</div>
                </div>
            </div>

        </div>

    </div>

</%block>