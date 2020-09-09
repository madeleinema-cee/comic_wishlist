<div class="panel-collapse collapse in" id="pub{{loop.index0}}">
            {% for title, issues in comic_list.items() %}
                <ul class="list-group">
                    <li class="list-group-item py-1">
                        <div class="row">
                            <div class="col-4">
                                <a class="title" data-toggle="collapse" href="#title{{issues[0]['title_id']}}" role="button" aria-expanded="false" aria-controls="collapse" onclick="toggleHidden('{{issues[0]['title_id']}}'); replaceIcon('chevron{{issues[0]['title_id']}}', 'fa-chevron-down', 'fa-chevron-up') ">
                                    {{title}}<i class='fas fa-chevron-down' id="chevron{{issues[0]['title_id']}}"></i>
                                </a>
                            </div>

                            <div class="col-3 subtitle"><small>{{issues|length}}<i class="fas fa-book"></i></small></div>
                            <div class="col-5 subtitle">
                                {{issues[0]['cover_desc']}}
                            </div>
                        </div>

                        <ul class="list-group list-group-flush collapse" id="title{{issues[0]['title_id']}}">
                            {% for issue in issues %}
                                <li class="list-group-item py-1">
                                    <div class="row">
                                        <div class="col-4">
                                            <small>{{issue['issue_number']}} {{issue['desc']}}</small>
                                        </div>
                                        <div class="col-3">
                                            <small>{{issue['color']}}-{{issue['score']}} {{issue['comment']}}</small>
                                        </div>

                                        <div class="col-2">
                                            <a data-toggle="modal" data-target="#issue{{issue['issue_id']}}" onclick="lazyLoadImage('img{{issue['issue_id']}}')">
                                                <small><i class='far fa-file-image issue'></i></small>
                                            </a>
                                        </div>
                                        <div class="col-3">
                                            <small class="date">{{issue['date']}}</small>
                                        </div>
                                    </div>
                                    <div class="modal fade" id="issue{{issue['issue_id']}}" tabindex="-1" role="dialog"
                                         aria-labelledby="ModalLabel" aria-hidden="true">
                                        <div class="modal-dialog modal-dialog-centered" role="document">
                                            <div class="modal-content">
                                                <button type="button" class="close" data-dismiss="modal"
                                                        aria-label="Close"><span aria-hidden="true">&times;</span>
                                                </button>
                                                <img data-src="http://images.comiccollectorlive.com/covers/{{issue['cover_id']}}/{{issue['issue_id']}}.jpg" id="img{{issue['issue_id']}}" alt="comic-image" data-loaded="0">
                                            </div>
                                        </div>
                                    </div>
                                </li>
                            {% endfor %}
                        </ul>
                    </li>
                </ul>
            {%endfor%}
        </div>
    </div>