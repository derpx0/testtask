from django.shortcuts import render
from django.http import HttpResponse
from .models import Picture, PictureTag
from test_task import settings
import dataset_utils

SORT_UNSORTED = 0
SORT_TIME = 1
SORT_LIKES = 2

PICS_PER_PAGE = 20

def dev_filltags(request):
    """
    :param request: http request
    :return: http response

    Development function
    Assigns a randomly selected set of tags to each picture in the database
    """
    if not settings.DEVELOPMENT:
        return HttpResponse('Disabled')

    dataset_utils.tag_pictures(True)
    return HttpResponse('All pictures were randomly tagged')

def dev_filllikes(request):
    """
    :param request: http request
    :return: http response

    Development function
    Assigns a random number of likes for each picture in the database
    """
    if not settings.DEVELOPMENT:
        return HttpResponse('Disabled')

    dataset_utils.place_likes()
    return HttpResponse('All pictures were randomly liked')

def view_pics(request):
    """
    :param request: http request
    :return: http response

    View a pic filled page
    """

    def move_page(qs, page_n, page_size):
        if qs.count() < page_n * page_size:
            return False, list()
        else:
            return True, qs[page_n * page_size: page_n * page_size + page_size]

    page = int(request.GET.get('page', 0))
    tag_names = request.GET.getlist('tag')
    exclude_tags = request.GET.getlist('etag')
    sort_method = int(request.GET.get('order', 0))
    if sort_method not in (SORT_UNSORTED, SORT_TIME, SORT_LIKES):
        sort_method = SORT_UNSORTED

    pics = None
    context = dict()

    tags = PictureTag.objects.filter(title__in=tag_names)
    etags = PictureTag.objects.filter(title__in=exclude_tags)

    for tag in tags:
        if pics is None:
            pics = tag.tagLinks.all()
        else:
            pics &= tag.tagLinks.all()

    if pics is None:
        pics = Picture.objects.all()

    for etag in etags:
        if pics is not None:
            pics = pics.exclude(id__in=[ep.id for ep in etag.tagLinks.all()])

    if sort_method == SORT_TIME:
        pics = pics.order_by('-timestamp')
    elif sort_method == SORT_LIKES:
        pics = pics.order_by('-userLikes')

    in_bounds, pic_page = move_page(pics, page, PICS_PER_PAGE)
    if not in_bounds:
        return HttpResponse('404')

    context['pics'] = list()
    for pic in pic_page:
        pic_obj = dict()
        pic_obj['src'] = pic.location
        pic_obj['time'] = pic.timestamp
        pic_obj['likes'] = pic.userLikes
        pic_obj['tags'] = map(lambda t: t['title'], pic.picturetag_set.all().values())
        pic_obj['owner'] = pic.owner.userName
        context['pics'].append(pic_obj)

    return render(request, 'picview/picview.html', context)